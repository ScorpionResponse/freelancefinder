"""Harvest process for the HackerNews Source."""

import datetime
import itertools
import logging
from collections import defaultdict

import bleach
from hackernews import HackerNews, InvalidItemID

from jobs.models import Post

logger = logging.getLogger(__name__)


class Harvester(object):
    """Simple Harvester to gather hackernews posts."""

    def __init__(self, source):
        """Init the hackernews harvester."""
        self.source = source
        self.client = HackerNews()
        self.status_info = defaultdict(int)

    def harvest(self):
        """Gather some Posts from hackernews."""
        self._check_for_new_hiring_threads()
        for post in itertools.chain(self._process_job_stories(), self._process_threads()):
            yield post
        logger.info("HackerNews harvester status: %s", dict(self.status_info))

    def _process_job_stories(self):
        """Process the job_stories from hackernews."""
        for story_id in self.client.job_stories(limit=100):
            story = self.client.get_item(story_id)
            if Post.objects.filter(source=self.source, unique=story.item_id).exists():
                logger.info("HackerNews harvester got duplicate post id %s, assuming everything new is harvested.", story.item_id)
                break
            else:
                desc = ''
                if story.text:
                    desc = story.text
                url = story.url
                if not url:
                    url = "https://news.ycombinator.com/item?id={}".format(story.item_id)
                post = Post(url=url, source=self.source, title=bleach.clean(story.title[:255], strip=True), description=desc, unique=story.item_id, created=story.submission_time, subarea='jobs', is_job_posting=True)
                self.status_info['count-job'] += 1
                self.status_info['total'] += 1
                yield post

    def _check_for_new_hiring_threads(self):
        """Find new hiring posts from the whoishiring user."""
        month_year = datetime.date.today().strftime("%B %Y")
        if self.source.config.filter(config_key='processed_date-last_month', config_value=month_year).exists():
            return
        who_is_hiring_user = self.client.get_user('whoishiring')
        new_posts = [False, False, False]
        for post_id in who_is_hiring_user.submitted[:7]:
            hn_item = self.client.get_item(post_id)
            if month_year in hn_item.title:
                if 'Who is hiring?' in hn_item.title:
                    new_posts[0] = post_id
                if 'Freelancer? Seeking freelancer?' in hn_item.title:
                    new_posts[1] = post_id
                if 'Who wants to be hired?' in hn_item.title:
                    new_posts[2] = post_id

        if all(new_posts):
            self.source.config.update_or_create(config_key='processed_date-last_month', defaults={'config_value': month_year})
            self.source.config.update_or_create(config_key='post_id-who_is_hiring', defaults={'config_value': new_posts[0]})
            self.source.config.update_or_create(config_key='post_id-freelancer', defaults={'config_value': new_posts[1]})
            self.source.config.update_or_create(config_key='post_id-who_wants_to_be_hired', defaults={'config_value': new_posts[2]})

    def _process_threads(self):
        """Process each hiring thread."""
        return itertools.chain(
            self._process_who_is_hiring(),
            self._process_who_wants_to_be_hired(),
            self._process_freelancer()
        )

    def _process_who_is_hiring(self):
        """Process the Who is hiring? thread."""
        today = datetime.date.today().strftime("%Y-%m-%d")
        if self.source.config.filter(config_key='processed_date-who_is_hiring', config_value=today).exists():
            return
        logger.info("Processing who is hiring post")
        post_id = self.source.config.filter(config_key='post_id-who_is_hiring').first().config_value
        hn_item = self.client.get_item(post_id)
        # r'\s*(?P<company>[^|]+?)\s*\|\s*(?P<title>[^|]+?)\s*\|\s*(?P<locations>[^|]+?)\s*(?:\|\s*(?P<attrs>.+))?$'
        for comment_id in hn_item.kids:
            if Post.objects.filter(source=self.source, unique=comment_id).exists():
                logger.debug('Already processed comment %s.', comment_id)
                continue
            try:
                comment = self.client.get_item(comment_id)
            except InvalidItemID as iiid:
                logger.warning('Tried to get non-existent comment with ID: %s; ex: %s', comment_id, iiid)
                continue
            if comment.text is None:
                logger.debug("Skipping blank comment: %s", comment)
                continue
            url = "https://news.ycombinator.com/item?id={}".format(comment_id)
            title = bleach.clean(comment.text.split('<')[0][:255], strip=True)
            post = Post(url=url, source=self.source, title=title, description=comment.text, unique=comment_id, created=comment.submission_time, subarea='who_is_hiring', is_job_posting=True)
            self.status_info['count-who_is_hiring'] += 1
            self.status_info['total'] += 1
            yield post
        self.source.config.update_or_create(config_key='processed_date-who_is_hiring', defaults={'config_value': today})

    def _process_who_wants_to_be_hired(self):
        """Process the Who wants to be hired? thread."""
        today = datetime.date.today().strftime("%Y-%m-%d")
        if self.source.config.filter(config_key='processed_date-who_wants_to_be_hired', config_value=today).exists():
            return
        logger.info("Processing who wants to be hired post")
        post_id = self.source.config.filter(config_key='post_id-who_wants_to_be_hired').first().config_value
        hn_item = self.client.get_item(post_id)
        for comment_id in hn_item.kids:
            if Post.objects.filter(source=self.source, unique=comment_id).exists():
                logger.debug('Already processed comment %s.', comment_id)
                continue
            try:
                comment = self.client.get_item(comment_id)
            except InvalidItemID as iiid:
                logger.warning('Tried to get non-existent comment with ID: %s; ex: %s', comment_id, iiid)
                continue
            if comment.text is None:
                logger.debug("Skipping blank comment: %s", comment)
                continue
            url = "https://news.ycombinator.com/item?id={}".format(comment_id)
            title = bleach.clean(comment.by + ' - ' + comment.text.split('<')[0], strip=True)
            post = Post(url=url, source=self.source, title=title[:255], description=comment.text, unique=comment_id, created=comment.submission_time, subarea='who_wants_to_be_hired', is_freelancer=True)
            self.status_info['count-who_wants_to_be_hired'] += 1
            self.status_info['total'] += 1
            yield post
        self.source.config.update_or_create(config_key='processed_date-who_wants_to_be_hired', defaults={'config_value': today})

    def _process_freelancer(self):
        """Process the Freelancer/Seeking freelancer? thread."""
        today = datetime.date.today().strftime("%Y-%m-%d")
        if self.source.config.filter(config_key='processed_date-freelancer', config_value=today).exists():
            return
        logger.info("Processing freelancer post")
        post_id = self.source.config.filter(config_key='post_id-freelancer').first().config_value
        hn_item = self.client.get_item(post_id)
        for comment_id in hn_item.kids:
            if Post.objects.filter(source=self.source, unique=comment_id).exists():
                logger.debug('Already processed comment %s.', comment_id)
                continue
            try:
                comment = self.client.get_item(comment_id)
            except InvalidItemID as iiid:
                logger.warning('Tried to get non-existent comment with ID: %s; ex: %s', comment_id, iiid)
                continue
            if comment.text is None:
                logger.debug("Skipping blank comment: %s", comment)
                continue
            url = "https://news.ycombinator.com/item?id={}".format(comment_id)
            title = bleach.clean(comment.by + ' - ' + comment.text.split('<')[0], strip=True)
            post = Post(url=url, source=self.source, title=title[:255], description=comment.text, unique=comment_id, created=comment.submission_time, subarea='freelancer', is_freelance=True)
            if 'SEEKING WORK' in title.upper():
                post.is_freelancer = True
            elif 'SEEKING FREELANCER' in title.upper():
                post.is_job_posting = True
            self.status_info['count-freelancer'] += 1
            self.status_info['total'] += 1
            yield post
        self.source.config.update_or_create(config_key='processed_date-freelancer', defaults={'config_value': today})

    def status(self):
        """Return the current status of this harvester."""
        return self.status_info

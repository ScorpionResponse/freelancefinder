"""Wrapper for hackernews."""

import datetime
import logging

import bleach
import hackernews

from django.utils import timezone

from jobs.models import Post

logger = logging.getLogger(__name__)


class HackerHarvest(object):
    """Wrapper client for hackernews harvester."""

    def __init__(self, source):
        """Initialize the harvester."""
        self.source = source
        self.client = hackernews.HackerNews()

    def job_stories(self):
        """Gather job postings and turn them into posts."""
        for story_id in self.client.job_stories(limit=100):
            try:
                story = self.client.get_item(story_id)
            except hackernews.InvalidItemID as iiid:
                logger.warning('Tried to get non-existent job story with ID: %s; ex: %s', story_id, iiid)
                continue
            post = self.parse_job_to_post(story, subarea='jobs')
            post.title = 'Full Time - {}'.format(post.title)
            post.title = post.title[:255]
            yield post

    def hiring_jobs(self):
        """Gather posts from the Who is Hiring? thread."""
        post_id = self.source.config.filter(config_key='post_id-who_is_hiring').first().config_value
        hn_item = self.client.get_item(post_id)
        # r'\s*(?P<company>[^|]+?)\s*\|\s*(?P<title>[^|]+?)\s*\|\s*(?P<locations>[^|]+?)\s*(?:\|\s*(?P<attrs>.+))?$'
        for comment_id in hn_item.kids:
            try:
                comment = self.client.get_item(comment_id)
            except hackernews.InvalidItemID as iiid:
                logger.warning('Tried to get non-existent comment with ID: %s; ex: %s', comment_id, iiid)
                continue
            if comment.text is None:
                logger.debug("Skipping blank comment: %s", comment)
                continue
            post = self.parse_job_to_post(comment, subarea='who_is_hiring')
            post.title = 'Hiring - {}'.format(post.title)
            post.title = post.title[:255]
            yield post

    def who_wants_jobs(self):
        """Gather posts from the Who wants to be hired? thread."""
        post_id = self.source.config.filter(config_key='post_id-who_wants_to_be_hired').first().config_value
        hn_item = self.client.get_item(post_id)
        for comment_id in hn_item.kids:
            try:
                comment = self.client.get_item(comment_id)
            except hackernews.InvalidItemID as iiid:
                logger.warning('Tried to get non-existent comment with ID: %s; ex: %s', comment_id, iiid)
                continue
            if comment.text is None:
                logger.debug("Skipping blank comment: %s", comment)
                continue
            post = self.parse_job_to_post(comment, subarea='who_wants_to_be_hired', insert_author=True)
            post.title = 'For Hire - {}'.format(post.title)
            post.title = post.title[:255]
            yield post

    def freelancer_jobs(self):
        """Gather posts from the Freelancers thread."""
        post_id = self.source.config.filter(config_key='post_id-freelancer').first().config_value
        hn_item = self.client.get_item(post_id)
        for comment_id in hn_item.kids:
            try:
                comment = self.client.get_item(comment_id)
            except hackernews.InvalidItemID as iiid:
                logger.warning('Tried to get non-existent comment with ID: %s; ex: %s', comment_id, iiid)
                continue
            if comment.text is None:
                logger.debug("Skipping blank comment: %s", comment)
                continue
            post = self.parse_job_to_post(comment, subarea='freelancer', insert_author=True)
            if 'SEEKING WORK' in post.title.upper():
                post.title = 'For Hire - {}'.format(post.title)
            elif 'SEEKING FREELANCER' in post.title.upper():
                post.title = 'Freelance - {}'.format(post.title)
                # TODO(Paul): Just set the is_freelance flag?
                post.is_freelance = True
            post.title = post.title[:255]
            yield post

    def check_who_is_hiring(self):
        """Check for new who is hiring posts every month."""
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

    def parse_job_to_post(self, job_info, subarea, insert_author=False):
        """Convert a comment or story to a Post."""
        title = job_info.title
        if title is None:
            title = job_info.text.split('<')[0]
        if insert_author:
            title = job_info.by + ' - ' + title
        title_cleaned = bleach.clean(title[:255], strip=True)
        desc = ''
        if job_info.text:
            desc = job_info.text
        url = job_info.url
        if not url:
            url = "https://news.ycombinator.com/item?id={}".format(job_info.item_id)
        created = timezone.make_aware(job_info.submission_time, is_dst=False)
        post = Post(url=url, source=self.source, title=title_cleaned, description=desc, unique=job_info.item_id, created=created, subarea=subarea)
        return post

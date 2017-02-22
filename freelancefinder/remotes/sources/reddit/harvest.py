"""Harvest process for the Reddit Source."""

import logging
import praw

from django.conf import settings

from jobs.models import Post

logger = logging.getLogger(__name__)


class Harvester(object):
    """Simple Harvester to gather reddit posts."""

    def __init__(self, source):
        """Init the harvester with basic info."""
        self.source = source
        self.status_info = {'count': 0}
        self.client = praw.Reddit(client_id=settings.REDDIT_CLIENT_ID,
                                  client_secret=settings.REDDIT_CLIENT_SECRET,
                                  user_agent=settings.REDDIT_USER_AGENT)

    def harvest(self):
        """Gather some Posts from reddit."""
        subreddits_to_monitor = self.source.config.filter(config_key='subreddits').first().config_value.split('|')
        subreddit_joined = '+'.join(subreddits_to_monitor)
        for submission in self.client.subreddit(subreddit_joined).new(limit=100):
            if Post.objects.filter(source=self.source, unique=submission.id).exists():
                logger.info("Reddit harvester got duplication post id %s, assuming everything new is harvested.", submission.id)
                break
            else:
                post = Post(url=submission.url, source=self.source, title=submission.title[:255], description=submission.selftext, unique=submission.id)
                self.status_info['count'] += 1
                yield post
        logger.info("Reddit harvester got %s posts", self.status_info['count'])

    def status(self):
        """Return the current status of this harvester."""
        return self.status_info

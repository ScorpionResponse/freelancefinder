"""Harvest process for the Reddit Source."""

from collections import defaultdict
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
        self.status_info = defaultdict(int)
        self.client = praw.Reddit(client_id=settings.REDDIT_CLIENT_ID,
                                  client_secret=settings.REDDIT_CLIENT_SECRET,
                                  user_agent=settings.REDDIT_USER_AGENT)

    def harvest(self):
        """Gather some Posts from reddit."""
        subreddits_to_monitor = self.source.config.filter(config_key='subreddits').first().config_value.split('|')
        for subr in subreddits_to_monitor:
            for submission in self.client.subreddit(subr).new(limit=100):
                if Post.objects.filter(source=self.source, unique=submission.id).exists():
                    logger.info("Reddit harvester got duplication post id %s in subreddit %s, assuming everything new is harvested.", submission.id, subr)
                    break
                else:
                    post = Post(url=submission.url, source=self.source, title=submission.title[:255], description=submission.selftext, unique=submission.id, subarea=submission.subreddit)
                    self.status_info['count-%s' % (subr,)] += 1
                    self.status_info['total'] += 1
                    yield post
        logger.info("Reddit harvester status: %s", dict(self.status_info))

    def status(self):
        """Return the current status of this harvester."""
        return self.status_info

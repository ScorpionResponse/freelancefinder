"""Harvest process for the Reddit Source."""

import praw

from django.conf import settings

from jobs.models import Post


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
        subreddits_to_monitor = self.source.config['subreddits']
        subreddit_joined = '+'.join(subreddits_to_monitor)
        for submission in self.client.subreddit(subreddit_joined).new(limit=10):
            if not Post.objects.filter(source=self.source, unique=submission.id).exists():
                post = Post(url=submission.url, source=self.source, title=submission.title, description=submission.selftext, unique=submission.id)
                self.status_info['count'] += 1
                yield post

    def status(self):
        """Return the current status of this harvester."""
        return self.status_info

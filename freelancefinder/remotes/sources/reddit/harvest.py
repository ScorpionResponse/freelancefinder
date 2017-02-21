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
        for index in range(10):
            post = Post(url="http://reddit.com/", source=self.source, title="Test Post {}".format(index), description="Steve")
            self.status_info['count'] += 1
            yield post

    def status(self):
        """Return the current status of this harvester."""
        return self.status_info

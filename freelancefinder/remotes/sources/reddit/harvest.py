"""Harvest process for the Reddit Source."""

from jobs.models import Post


class Harvester(object):
    """Simple Harvester to gather reddit posts."""

    def __init__(self, code, name):
        """Init the harvester with basic info."""
        self.code = code
        self.name = name

    def harvest(self):
        """Gather some Posts from reddit."""
        for index in range(10):
            post = Post(url="http://reddit.com/", title="Test Post {}".format(index), description="Steve")
            yield post

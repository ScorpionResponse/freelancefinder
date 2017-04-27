"""Harvest process for the Reddit Source."""

from collections import defaultdict
import logging

from remotes.decorators import periodically
from .reddit import Reddit

logger = logging.getLogger(__name__)


class Harvester(object):
    """Simple Harvester to gather reddit posts."""

    def __init__(self, source):
        """Init the harvester with basic info."""
        self.source = source
        self.status_info = defaultdict(int)

    @periodically(period="minutely")
    def harvest(self):
        """Gather some Posts from reddit."""
        reddit = Reddit(self.source)
        for section in reddit.sections():
            logger.info("Reddit harvester retrieving subsection: %s", section)
            for post in reddit.jobs(section):
                if post.exists():
                    logger.info("Reddit harvester got duplication post id %s in subreddit %s, assuming everything new is harvested.", post, section)
                    break
                self.status_info['count-%s' % (section,)] += 1
                self.status_info['total'] += 1
                yield post

        logger.info("Reddit harvester status: %s", dict(self.status_info))

    def status(self):
        """Return the current status of this harvester."""
        return self.status_info

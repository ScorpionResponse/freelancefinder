"""Default Harvest Process."""

import logging
from collections import defaultdict

from remotes.decorators import periodically
from .rss_feed import RssFeed

logger = logging.getLogger(__name__)


class Harvester(object):
    """Simple Harvester to gather posts."""

    def __init__(self, source):
        """Init the harvester."""
        self.status_info = defaultdict(int)
        self.source = source

    @periodically(period='arg', fail_return=[])
    def harvest(self, frequency='daily'):
        """Gather some Posts."""
        logger.info("Harvesting %s at frequency %s", self.source, frequency)
        jobs = RssFeed(self.source)
        for post in jobs.jobs():
            if post.exists():
                logger.debug('Alread processed this item %s, skipping the rest.', post)
                break
            self.status_info['count-rss'] += 1
            self.status_info['total'] += 1
            yield post
        logger.info("RSS Feed harvester status: %s", dict(self.status_info))

    def status(self):
        """Return the current status of this harvester."""
        return self.status_info

"""Harvest process for the FossJobs Source."""

import logging
from collections import defaultdict

from remotes.decorators import periodically
from .fossjobs import FossJobs

logger = logging.getLogger(__name__)


class Harvester(object):
    """Simple Harvester to gather FossJobs posts."""

    def __init__(self, source):
        """Init the fossjobs harvester."""
        self.status_info = defaultdict(int)
        self.source = source

    @periodically(period='hourly')
    def harvest(self):
        """Gather some Posts from hackernews."""
        fossjobs = FossJobs(self.source)
        for post in fossjobs.jobs():
            if post.exists():
                logger.debug('Alread processed this item %s, skipping the rest.', post)
                break
            self.status_info['count-rss'] += 1
            self.status_info['total'] += 1
            yield post
        logger.info("FossJobs harvester status: %s", dict(self.status_info))

    def status(self):
        """Return the current status of this harvester."""
        return self.status_info

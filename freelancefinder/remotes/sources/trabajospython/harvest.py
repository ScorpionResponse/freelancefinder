"""Harvest process for the TrabajosPython Source."""

import logging
from collections import defaultdict

from remotes.decorators import periodically
from .trabajospython import TrabajosPython

logger = logging.getLogger(__name__)


class Harvester(object):
    """Simple Harvester to gather TrabajosPython posts."""

    def __init__(self, source):
        """Init the harvester."""
        self.status_info = defaultdict(int)
        self.source = source

    @periodically(period='daily', fail_return=[])
    def harvest(self):
        """Gather some Posts from trabajosPython."""
        trabajos = TrabajosPython(self.source)
        for post in trabajos.jobs():
            if post.exists():
                logger.debug('Alread processed this item %s, skipping the rest.', post)
                break
            self.status_info['count-rss'] += 1
            self.status_info['total'] += 1
            yield post
        logger.info("TrabajosPython harvester status: %s", dict(self.status_info))

    def status(self):
        """Return the current status of this harvester."""
        return self.status_info

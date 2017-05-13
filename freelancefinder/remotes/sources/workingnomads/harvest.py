"""Harvest process for the WorkingNomads Source."""

import logging
from collections import defaultdict

from remotes.decorators import periodically
from .workingnomads import WorkingNomads

logger = logging.getLogger(__name__)


class Harvester(object):
    """Simple Harvester to gather WorkingNomads posts."""

    def __init__(self, source):
        """Init the harvester."""
        self.status_info = defaultdict(int)
        self.source = source

    @periodically(period='twice_daily', fail_return=[])
    def harvest(self):
        """Gather some Posts from WorkingNomads."""
        nomads = WorkingNomads(self.source)
        for post in nomads.jobs():
            if post.exists():
                logger.debug('Alread processed this item %s, skipping and processing the rest.', post)
                continue
            self.status_info['count-api'] += 1
            self.status_info['total'] += 1
            yield post
        logger.info("WorkingNomads harvester status: %s", dict(self.status_info))

    def status(self):
        """Return the current status of this harvester."""
        return self.status_info

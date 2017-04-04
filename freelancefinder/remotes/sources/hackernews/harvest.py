"""Harvest process for the HackerNews Source."""

import itertools
import logging
from collections import defaultdict

from remotes.decorators import periodically

from .hackernews_wrapper import HackerHarvest

logger = logging.getLogger(__name__)


class Harvester(object):
    """Simple Harvester to gather hackernews posts."""

    def __init__(self, source):
        """Init the hackernews harvester."""
        self.source = source
        self.hackernews = HackerHarvest(self.source)
        self.status_info = defaultdict(int)

    def harvest(self):
        """Gather some Posts from hackernews."""
        self._check_for_new_hiring_threads()
        for post in itertools.chain(self._process_job_stories(), self._process_threads()):
            yield post
        logger.info("HackerNews harvester status: %s", dict(self.status_info))

    @periodically(period='daily', check_name='last_processed-job_stories')
    def _process_job_stories(self):
        """Process the job_stories from hackernews."""
        for post in self.hackernews.job_stories():
            if post.exists():
                logger.info("HackerNews harvester got duplicate post id %s, assuming everything new is harvested.", post)
                break

            self.status_info['count-job'] += 1
            self.status_info['total'] += 1
            yield post

    @periodically(period='daily', check_name='last_processed-new_threads')
    def _check_for_new_hiring_threads(self):
        """Find new hiring posts from the whoishiring user."""
        self.hackernews.check_who_is_hiring()

    def _process_threads(self):
        """Process each hiring thread."""
        return itertools.chain(
            self._process_who_is_hiring(),
            self._process_who_wants_to_be_hired(),
            self._process_freelancer()
        )

    @periodically(period='daily', check_name='last_processed-who_is_hiring')
    def _process_who_is_hiring(self):
        """Process the Who is hiring? thread."""
        logger.info("Processing who is hiring post")
        for post in self.hackernews.hiring_jobs():
            if post.exists():
                logger.debug('Already processed %s.', post)
                continue
            self.status_info['count-who_is_hiring'] += 1
            self.status_info['total'] += 1
            yield post

    @periodically(period='daily', check_name='last_processed-who_wants_to_be_hired')
    def _process_who_wants_to_be_hired(self):
        """Process the Who wants to be hired? thread."""
        logger.info("Processing who wants to be hired post")
        for post in self.hackernews.who_wants_jobs():
            if post.exists():
                logger.debug('Already processed %s.', post)
                continue
            self.status_info['count-who_wants_to_be_hired'] += 1
            self.status_info['total'] += 1
            yield post

    @periodically(period='daily', check_name='last_processed-freelancer')
    def _process_freelancer(self):
        """Process the Freelancer/Seeking freelancer? thread."""
        logger.info("Processing freelancer post")
        for post in self.hackernews.freelancer_jobs():
            if post.exists():
                logger.debug('Already processed %s.', post)
                continue
            self.status_info['count-freelancer'] += 1
            self.status_info['total'] += 1
            yield post

    def status(self):
        """Return the current status of this harvester."""
        return self.status_info

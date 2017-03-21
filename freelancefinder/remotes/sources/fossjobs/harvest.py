"""Harvest process for the FossJobs Source."""

import datetime
import logging
from collections import defaultdict

import bleach
import feedparser

from jobs.models import Post

logger = logging.getLogger(__name__)


class Harvester(object):
    """Simple Harvester to gather FossJobs posts."""

    def __init__(self, source):
        """Init the fossjobs harvester."""
        self.source = source
        self.status_info = defaultdict(int)

    def harvest(self):
        """Gather some Posts from hackernews."""
        today = datetime.date.today().strftime("%Y-%m-%d")
        if self.source.config.filter(config_key='processed_date-rss_feed', config_value=today).exists():
            return
        rss_feed = feedparser.parse('https://www.fossjobs.net/rss/all/')
        for job_info in rss_feed.entries:
            if Post.objects.filter(source=self.source, unique=job_info.id).exists():
                logger.debug('Alread processed this item %s, skipping the rest.', job_info.id)
                break
            post = Post(url=job_info.link, source=self.source, title=job_info.title, description=bleach.clean(job_info.description, strip=True), unique=job_info.id, subarea='all', is_job_posting=True)
            yield post
        logger.info("FossJobs harvester status: %s", dict(self.status_info))
        self.source.config.update_or_create(config_key='processed_date-rss_feed', defaults={'config_value': today})

    def status(self):
        """Return the current status of this harvester."""
        return self.status_info

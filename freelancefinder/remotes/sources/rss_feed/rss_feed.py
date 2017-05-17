"""Wrapper for the RSS Feed source."""

import datetime
import logging

import bleach
import feedparser

from django.utils import timezone

from jobs.models import Post

logger = logging.getLogger(__name__)

ADDITIONAL_TAGS = ['p', 'br']


class RssFeed(object):
    """Wrapper for the RssFeed source."""

    def __init__(self, source):
        """Parse the API."""
        self.source = source
        self.rss_address = self.source.config.filter(config_key='rss_feed_address').first().config_value
        self.rss_feed = feedparser.parse(self.rss_address)

    def jobs(self):
        """Iterate through all available jobs."""
        for job_info in self.rss_feed.entries:
            post = self.parse_job_to_post(job_info)
            yield post

    def parse_job_to_post(self, job_info):
        """Convert from the rss feed format to a Post."""
        logger.debug("Parsing: %s", job_info)
        try:
            created = timezone.make_aware(datetime.datetime(*job_info.published_parsed[0:6]), is_dst=False)
        except AttributeError:
            try:
                created = timezone.make_aware(datetime.datetime(*job_info.updated_parsed[0:6]), is_dst=False)
            except AttributeError:
                created = timezone.now()
        try:
            my_id = job_info.id
        except AttributeError:
            my_id = job_info.link
        post = Post(
            url=job_info.link,
            source=self.source,
            title=job_info.title,
            description=bleach.clean(job_info.description, tags=bleach.ALLOWED_TAGS + ADDITIONAL_TAGS, strip=True),
            unique=my_id,
            created=created,
            subarea='all',
        )
        return post

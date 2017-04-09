"""Wrapper for the FossJobs source."""

import datetime

import bleach
import feedparser

from django.utils import timezone

from jobs.models import Post

ADDITIONAL_TAGS = ['p', 'br']


class FossJobs(object):
    """Wrapper for the FossJobs source."""

    all_rss_address = 'https://www.fossjobs.net/rss/all/'

    def __init__(self, source, rss_source_feed=None):
        """Parse the feed or accept the incoming one (for testing)."""
        if rss_source_feed is not None:
            self.rss_feed = rss_source_feed
        else:
            self.rss_feed = feedparser.parse(self.all_rss_address)
        self.source = source

    def jobs(self):
        """Iterate through all available jobs."""
        for job_info in self.rss_feed.entries:
            post = self.parse_job_to_post(job_info)
            yield post

    def parse_job_to_post(self, job_info):
        """Convert from the rss feed format to a Post."""
        created = timezone.make_aware(datetime.datetime(*job_info.updated_parsed[0:6]), is_dst=False)
        post = Post(
            url=job_info.link,
            source=self.source,
            title=job_info.title,
            description=bleach.clean(job_info.description, tags=bleach.ALLOWED_TAGS + ADDITIONAL_TAGS, strip=True),
            unique=job_info.id,
            created=created,
            subarea='all',
            is_job_posting=True
        )
        return post

"""Wrapper for Reddit API."""

import datetime

import praw

from django.conf import settings
from django.utils import timezone

from jobs.models import Post


class Reddit(object):
    """Wrapper for the reddit API."""

    def __init__(self, source):
        """Init the reddit api client."""
        self.source = source
        self.client = praw.Reddit(client_id=settings.REDDIT_CLIENT_ID,
                                  client_secret=settings.REDDIT_CLIENT_SECRET,
                                  user_agent=settings.REDDIT_USER_AGENT)

    def sections(self):
        """Return the sections we'll be harvesting."""
        subreddits_to_monitor = self.source.config.filter(config_key='subreddits').first().config_value.split('|')
        for subr in subreddits_to_monitor:
            yield subr

    def jobs(self, section):
        """Get all jobs from a section/subreddit."""
        for submission in self.client.subreddit(section).new(limit=100):
            post = self.parse_job_to_post(submission)
            yield post

    def parse_job_to_post(self, job_info):
        """Convert reddit api response to a Post."""
        created_time = timezone.make_aware(datetime.datetime.utcfromtimestamp(job_info.created_utc))
        post = Post(url=job_info.permalink, source=self.source, title=job_info.title[:255], description=job_info.selftext, unique=job_info.id, subarea=job_info.subreddit, created=created_time)
        return post

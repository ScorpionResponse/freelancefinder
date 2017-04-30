"""Wrapper for the WorkInStartups source."""

import json

import bleach
import maya
import requests

from jobs.models import Post

ADDITIONAL_TAGS = ['p', 'br']


class WorkInStartups(object):
    """Wrapper for the WorkInStartups source."""

    json_api_address = 'http://workinstartups.com/job-board/api/api.php?action=getJobs&type=0&category=0&count=100&random=0&days_behind=0&response=json'

    def __init__(self, source):
        """Parse the API."""
        self.api_response = requests.get(self.json_api_address)
        self.source = source

    def jobs(self):
        """Iterate through all available jobs."""
        # Remove the 'var jobs = ' at the beginning and the ';' at the end
        response_json = json.loads(self.api_response.text[len("var jobs = "):-1])
        for job_info in response_json:
            post = self.parse_job_to_post(job_info)
            yield post

    def parse_job_to_post(self, job_info):
        """Convert from the rss feed format to a Post."""
        created = maya.parse(job_info['mysql_date']).datetime()
        job_url = 'http://workinstartups.com/job-board/job/{}/{}/'.format(job_info['id'], job_info['url_title'])
        post = Post(
            url=job_url,
            source=self.source,
            title=job_info['type_name'] + " - " + job_info['title'],
            description=bleach.clean(job_info['description'], tags=bleach.ALLOWED_TAGS + ADDITIONAL_TAGS, strip=True),
            unique=job_info['id'],
            created=created,
            subarea='all',
        )
        return post

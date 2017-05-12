"""Wrapper for the WorkingNomads source."""

import bleach
import maya
import requests

from jobs.models import Post

ADDITIONAL_TAGS = ['p', 'br']


class WorkingNomads(object):
    """Wrapper for the WorkingNomads source."""

    api_address = 'https://www.workingnomads.co/jobsapi/job/_search?sort=expired:asc,premium:desc,pub_date:desc&_source=company,category_name,description,location_base,instructions,id,external_id,slug,title,pub_date,tags,source,apply_url,premium,expired&size=50'

    def __init__(self, source):
        """Parse the api response."""
        self.api_response = requests.get(self.api_address).json()
        self.source = source

    def jobs(self):
        """Iterate through all available jobs."""
        for job_info in self.api_response['hits']['hits']:
            post = self.parse_job_to_post(job_info)
            yield post

    def parse_job_to_post(self, job_info):
        """Convert from the api response format to a Post."""
        created = maya.parse(job_info['_source']['pub_date'])
        url = 'https://www.workingnomads.co/jobs?job={}'.format(job_info['_source']['slug'])
        post = Post(
            url=url,
            source=self.source,
            title=job_info['_source']['title'],
            description=bleach.clean(job_info['_source']['description'], tags=bleach.ALLOWED_TAGS + ADDITIONAL_TAGS, strip=True),
            unique=job_info['_source']['id'],
            created=created,
            subarea=job_info['_source']['source'],
        )
        return post

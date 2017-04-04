"""Fixtures to create models in jobs app."""

import pytest

from remotes.models import Source
from ..models import Job, Post, Freelancer


@pytest.fixture
def post():
    """Generate a Post."""
    source = Source.objects.create(code='test_source', name='Test Source', url='http://test.example.com/')
    return Post.objects.create(url='http://test.example.com/', source=source, title='A New Post', description="Some Silly Description", unique='b')


@pytest.fixture
def freelancer():
    """Generate a Freelancer."""
    return Freelancer.objects.create(title='Another New Freelancer', description="Some Other Description")


@pytest.fixture
def job():
    """Generate a job."""
    return Job.objects.create(title='New Job', description="Some Description")

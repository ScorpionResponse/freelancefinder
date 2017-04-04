"""Tests related to Posts."""

import pytest

from remotes.models import Source
from ..models import Job, Post


def test_post_list(client, post):
    """Simple test for the posts list page."""
    response = client.get('/jobs/post-list/')
    assert response.status_code == 200


def test_post_list_filter_title(client, post):
    """Test filtering post list by title field."""
    response = client.get('/jobs/post-list/?title=test')
    assert response.status_code == 200


@pytest.mark.parametrize("field", ['is_job_posting', 'is_freelance', 'is_freelancer', 'is_not_classified'])
def test_post_list_filter_booleans(client, field, post):
    """Test filtering post list by title field."""
    response = client.get('/jobs/post-list/?{}=on'.format(field))
    assert response.status_code == 200


def test_create_post():
    """Test post creation."""
    source = Source.objects.create(code='test_source', name='Test Source', url='http://test.example.com/')
    post = Post.objects.create(url='http://test.example.com/', source=source, title='A New Post', description="Some Silly Description", unique='b')
    assert post is not None
    assert 'New Post' in str(post)

    num_posts = Post.objects.all().count()
    assert num_posts != 0


def test_create_post_with_job():
    """Test post creation."""
    source = Source.objects.create(code='test_source', name='Test Source', url='http://test.example.com/')
    job = Job.objects.create(title='A New Job', description="Some Description")
    post = Post.objects.create(job=job, url='http://test.example.com/', source=source, title='A New Post', description="Some Silly Description", unique='b')
    assert post is not None
    assert 'New Post' in str(post)

    num_posts = Post.objects.all().count()
    assert num_posts != 0


def test_get_posts(post):
    """Test that getting all posts works."""
    num_posts = Post.objects.all().count()
    assert num_posts != 0

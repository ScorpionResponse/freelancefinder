"""Tests related to Posts."""

import pytest

from remotes.models import Source
from ..models import Job, Post


def test_post_list(admin_group_client, post):
    """Simple test for the posts list page."""
    response = admin_group_client.get('/jobs/post-list/')
    assert response.status_code == 200


def test_post_list_with_100(admin_group_client, post_factory):
    """Simple test for the posts list page."""
    for i in range(100):
        new_post = post_factory()
    response = admin_group_client.get('/jobs/post-list/')
    assert response.status_code == 200


def test_post_list_filter_title(admin_group_client, post):
    """Test filtering post list by title field."""
    response = admin_group_client.get('/jobs/post-list/?title=test')
    assert response.status_code == 200


@pytest.mark.parametrize("field", ['is_job_posting', 'is_freelance', 'is_freelancer', 'is_not_classified'])
def test_post_list_filter_booleans(admin_group_client, field, post):
    """Test filtering post list by title field."""
    response = admin_group_client.get('/jobs/post-list/?{}=on'.format(field))
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


def test_post_action(admin_group_client, post):
    """Test that post action dismiss sets as garbage."""
    postdata = {
        'post_id': post.id,
        'dismiss': True,
    }
    response = admin_group_client.post('/jobs/post-action/', postdata)
    assert response.status_code == 302

    # Object is effectively hidden
    assert Post.objects.all().count() == 0
    assert not Post.objects.filter(pk=post.id).exists()

    # But still present
    for db_post in Post.objects.raw('SELECT id, garbage from jobs_post where id=%s' % post.id):
        assert db_post.garbage

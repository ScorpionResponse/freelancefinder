"""Tests related to jobs functionality."""


def test_job_list(client):
    """Simple test for the jobs list page."""
    response = client.get('/jobs/job-list/')
    assert response.status_code == 200


def test_post_list(client):
    """Simple test for the posts list page."""
    response = client.get('/jobs/post-list/')
    assert response.status_code == 200

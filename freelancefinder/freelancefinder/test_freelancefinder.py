"""
Tests for general parts of the FreelanceFinder application.

Anything which is not specific to only one module can go here.
"""


def test_homepage(client):
    """Simple test for the root page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'<html>' in response.content


def test_robots_txt(client):
    """Make sure we have a robots.txt file."""
    response = client.get('/robots.txt')
    assert response.status_code == 200


def test_humans_txt(client):
    """Make sure we have a humans.txt file."""
    response = client.get('/humans.txt')
    assert response.status_code == 200

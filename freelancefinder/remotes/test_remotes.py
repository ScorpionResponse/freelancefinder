"""Tests for the remotes app."""


def test_source_list(client):
    """Test source list page returns 200."""
    response = client.get('/remotes/source-list/')
    assert response.status_code == 200

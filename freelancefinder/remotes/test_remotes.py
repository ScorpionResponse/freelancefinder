"""Tests for the remotes app."""


def test_source_list(client):
    """Test source list page returns 200."""
    response = client.get('/remotes/source-list/')
    assert response.status_code == 200


def test_harvester():
    """Test that getting harvester returns something."""
    from .models import Source
    for source in Source.objects.all():
        harvester = source.harvester()
        assert harvester is not None

"""Tests for the remotes app."""

from .models import Source


def test_source_list(client):
    """Test source list page returns 200."""
    response = client.get('/remotes/source-list/')
    assert response.status_code == 200


def test_harvester():
    """Test that getting harvester returns something."""
    for source in Source.objects.all():
        harvester = source.harvester()
        assert harvester is not None


def test_add_source():
    """Add a source and test outcome."""
    start_count = Source.objects.all().count()
    new_source = Source.objects.create(code='new', name='New Source', url='http://test.example.com/')
    assert 'New Source' in str(new_source)
    assert new_source is not None
    assert Source.objects.all().count() == 1 + start_count

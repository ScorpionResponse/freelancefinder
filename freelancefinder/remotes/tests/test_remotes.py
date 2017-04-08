"""Tests for the remotes app."""

import pytest

from django.db import IntegrityError

from ..models import Source, SourceConfig


def test_source_list(debug_group_client):
    """Test source list page returns 200."""
    response = debug_group_client.get('/remotes/source-list/')
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


def test_source_config():
    """Simple source config test."""
    new_source = Source.objects.create(code='new', name='New Source', url='http://test.example.com/')
    conf = SourceConfig.objects.create(source=new_source, config_key='bob', config_value='jones')
    assert conf is not None
    assert 'bob' in str(conf)


def test_source_config_uniqueness():
    """Source Config should prevent the same keys."""
    new_source = Source.objects.create(code='new', name='New Source', url='http://test.example.com/')
    conf = SourceConfig.objects.create(source=new_source, config_key='bob', config_value='jones')
    assert conf is not None
    with pytest.raises(IntegrityError):
        SourceConfig.objects.create(source=new_source, config_key='bob', config_value='stevens')

"""Tests for TagVariants."""

from taggit.models import Tag

from ..models import TagVariant


def test_create():
    """Create a new tagvariant."""
    tag = Tag.objects.create(name='soup')
    new_tagv = TagVariant.objects.create(variant='Soup', tag=tag)
    assert new_tagv is not None
    assert 'Soup' in str(new_tagv)

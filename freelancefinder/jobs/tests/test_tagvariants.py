"""Tests for TagVariants."""

from ..models import TagVariant


def test_create():
    """Create a new tagvariant."""
    new_tagv = TagVariant.objects.create(variant='Soup')
    assert new_tagv is not None
    assert 'Soup' in str(new_tagv)

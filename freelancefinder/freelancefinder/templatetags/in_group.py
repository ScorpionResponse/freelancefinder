"""Check whether a user is in a group."""

from django import template

from users.utils import is_in_group

register = template.Library()


@register.filter(name='in_group')
def in_group_filter(user, groups):
    """Filter to return whether user is in a group."""
    return is_in_group(user, groups)

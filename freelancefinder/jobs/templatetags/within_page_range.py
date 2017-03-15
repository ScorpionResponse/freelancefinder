"""within_page_range template filter."""

import math

from django import template

register = template.Library()


@register.filter(name='within_page_range')
def within_filter(test_page, current_page):
    """Check whether test_page is within 10 of current_page."""
    return math.fabs(current_page - test_page) <= 10

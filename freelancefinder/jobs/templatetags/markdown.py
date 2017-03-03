"""Markdown template filter."""

from django import template

import bleach
import markdown

register = template.Library()


@register.filter(name='markdown', is_safe=True)
def markdown_filter(value):
    """Convert markdown value to html."""
    return bleach.clean(markdown.markdown(value))

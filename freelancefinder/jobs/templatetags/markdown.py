"""Markdown template filter."""

from django import template
from django.template.defaultfilters import stringfilter

import markdown

register = template.Library()


@register.filter(name='markdown', is_safe=True)
@stringfilter
def markdown_filter(value):
    """Convert markdown value to html."""
    return markdown.markdown(value)

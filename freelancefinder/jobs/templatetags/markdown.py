"""Markdown template filter."""

from django import template
from django.template.defaultfilters import stringfilter

import bleach
import markdown

register = template.Library()


@register.filter(is_safe=True, name='markdown')
@stringfilter
def markdown_filter(value):
    """Convert markdown value to html."""
    return bleach.clean(markdown.markdown(value))

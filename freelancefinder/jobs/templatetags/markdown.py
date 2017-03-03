"""Markdown template filter."""

from django import template
from django.utils.safestring import mark_safe

import bleach
import markdown

register = template.Library()


@register.filter(name='markdown')
def markdown_filter(value):
    """Convert markdown value to html."""
    rendered_html = markdown.markdown(value)
    bleached_html = bleach.clean(rendered_html, tags=bleach.ALLOWED_TAGS + ['p'])
    return mark_safe(bleached_html)

"""Markdown template filter."""

from django import template

import bleach
import markdown

register = template.Library()


@register.filter(name='markdown', is_safe=True)
def markdown_filter(value):
    """Convert markdown value to html."""
    import logging
    logger = logging.getLogger(__name__)
    description = bleach.clean(markdown.markdown(value), tags=bleach.ALLOWED_TAGS + ['p'])
    logger.info('Description: %s', description)
    return description

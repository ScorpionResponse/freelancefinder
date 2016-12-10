"""Simple views for no specific app."""
from django.views.generic.base import TemplateView


class IndexPageView(TemplateView):
    """A simple homepage template view."""

    template_name = 'index.html'

"""Views for remotes app."""
from django.views.generic import ListView

from .models import Source


class SourceListView(ListView):
    """List all Sources."""

    model = Source
    template_name = "remotes/source_list.html"

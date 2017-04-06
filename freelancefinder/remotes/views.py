"""Views for remotes app."""
from braces.views import GroupRequiredMixin

from django.views.generic import ListView

from .models import Source


class SourceListView(GroupRequiredMixin, ListView):
    """List all Sources."""

    model = Source
    group_required = u'Debuggers'
    template_name = "remotes/source_list.html"

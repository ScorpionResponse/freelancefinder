"""Views for remotes app."""
from braces.views import GroupRequiredMixin

from django.views.generic import ListView

from .models import Source
from .utils import get_harvest_history


class SourceListView(GroupRequiredMixin, ListView):
    """List all Sources."""

    model = Source
    group_required = u'Debuggers'
    template_name = "remotes/source_list.html"

    def get_context_data(self, **kwargs):
        """Add history to context info."""
        context = super(SourceListView, self).get_context_data(**kwargs)
        # Trim out the last 30 days, since we only want a snapshot
        context['harvest_history'] = get_harvest_history()
        return context

"""Views for remotes app."""
from braces.views import GroupRequiredMixin

from django.db.models.aggregates import Count
from django.db.models.functions.datetime import TruncDate
from django.views.generic import ListView

from .models import Source


class SourceListView(GroupRequiredMixin, ListView):
    """List all Sources."""

    model = Source
    group_required = u'Debuggers'
    template_name = "remotes/source_list.html"

    def _get_harvest_history(self):
        """Get a history of harvests executed."""
        history = Source.objects.all().values('code', harvest_date=TruncDate('posts__modified')).annotate(post_count=Count('posts')).order_by('-harvest_date', 'name')
        return history

    def get_context_data(self, **kwargs):
        """Add history to context info."""
        context = super(SourceListView, self).get_context_data(**kwargs)
        context['harvest_history'] = self._get_harvest_history()
        return context

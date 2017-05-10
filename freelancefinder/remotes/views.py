"""Views for remotes app."""
import logging

from braces.views import GroupRequiredMixin

from django.db.models.aggregates import Count
from django.db.models.functions.datetime import TruncDate
from django.views.generic import ListView

from .models import Source

logger = logging.getLogger(__name__)


class SourceListView(GroupRequiredMixin, ListView):
    """List all Sources."""

    model = Source
    group_required = u'Debuggers'
    template_name = "remotes/source_list.html"

    def _get_harvest_history(self):
        """Get a history of harvests executed."""
        harvest_table = []
        code_position = {}
        header = [(0, 'Harvest Date')]

        all_sources = Source.objects.all().values_list('code', 'name').order_by('name')
        for position, (code, name) in enumerate(all_sources, 1):
            code_position[code] = position
            header.append((position, name))

        history = Source.objects.all().values('code', harvest_date=TruncDate('posts__modified')).annotate(post_count=Count('posts')).order_by('-harvest_date')
        current_date = None
        this_row = header
        for row in history:
            if row['harvest_date'] != current_date:
                logger.debug('Appending info: %s', this_row)
                harvest_table.append([value for position, value in sorted(this_row)])
                this_row = []
                this_row.append((0, row['harvest_date']))
                current_date = row['harvest_date']
            this_row.append((code_position[row['code']], row['post_count']))

        return harvest_table

    def get_context_data(self, **kwargs):
        """Add history to context info."""
        context = super(SourceListView, self).get_context_data(**kwargs)
        context['harvest_history'] = self._get_harvest_history()
        return context

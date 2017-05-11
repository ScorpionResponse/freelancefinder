"""Utils for the remotes app."""
import logging
from datetime import datetime, timedelta

from django.db.models.aggregates import Count
from django.db.models.functions.datetime import TruncDate

from .models import Source

logger = logging.getLogger(__name__)


def get_harvest_history():
    """Get a history of harvests executed."""
    report_since_day = datetime.now() - timedelta(days=30)
    harvest_table = []
    code_position = {}
    header = [(0, 'Harvest Date')]

    all_sources = Source.objects.all().values_list('code', 'name').order_by('name')
    for position, (code, name) in enumerate(all_sources, 1):
        code_position[code] = position
        header.append((position, name))

    history = Source.objects.filter(posts__created__gte=report_since_day).values('code', harvest_date=TruncDate('posts__created')).annotate(post_count=Count('posts')).order_by('harvest_date')
    current_date = None
    this_row = header
    for row in history:
        logger.info("Processing source history row: %s", row)
        if row['harvest_date'] != current_date:
            if len(this_row) < len(code_position) + 1:
                # This is some kind of garbage that could be cleaned up
                this_row_dict = {k: v for k, v in this_row}
                new_row = []
                for position in range(len(code_position) + 1):
                    if position in this_row_dict:
                        new_row.append((position, this_row_dict[position]))
                    else:
                        new_row.append((position, 0))
                this_row = new_row
            logger.debug('Appending info: %s', this_row)
            harvest_table.append([value for position, value in sorted(this_row)])
            this_row = []
            this_row.append((0, row['harvest_date']))
            current_date = row['harvest_date']
        this_row.append((code_position[row['code']], row['post_count']))

    return harvest_table

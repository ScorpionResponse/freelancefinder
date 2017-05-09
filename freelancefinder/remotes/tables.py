"""Tables used for the remotes app."""
import django_tables2 as tables


class HistoryTable(tables.Table):
    """Define a table to display the history."""

    code = tables.Column()
    harvest_date = tables.Column()
    post_count = tables.Column()

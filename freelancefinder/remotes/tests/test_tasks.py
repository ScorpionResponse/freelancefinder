"""Tests related to the remotes.tasks functions."""

from django_celery_beat.models import IntervalSchedule, PeriodicTask

from ..tasks import setup_periodic_tasks


def test_make_tasks():
    """Ensure that setup makes some tasks/schedules."""
    setup_periodic_tasks(None)
    intervals = IntervalSchedule.objects.all().count()
    tasks = PeriodicTask.objects.all().count()

    assert intervals > 0
    assert tasks > 0

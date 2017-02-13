"""Celery bootstrap and configuration process."""
import os

from celery import Celery

from django_celery_beat.models import IntervalSchedule, PeriodicTask


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freelancefinder.settings')

celery_app = Celery('freelancefinder')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks.py modules from all registered Django app configs.
celery_app.autodiscover_tasks()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Ensure periodic tasks are present in the DB."""

    schedule, created = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.minutes)

    PeriodicTask.get_or_create(interval=schedule, name='Harvest Remotes',
                               task='remotes.tasks.harvest_sources')

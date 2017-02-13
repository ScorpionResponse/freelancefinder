"""Tasks to perform periodic tasks with remotes."""

from django_celery_beat.models import IntervalSchedule, PeriodicTask
from celery import Celery
from celery.utils.log import get_task_logger


celery_app = Celery()
logger = get_task_logger(__name__)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Ensure periodic tasks are present in the DB."""

    schedule, created = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.MINUTES)

    PeriodicTask.get_or_create(interval=schedule, name='Harvest Remotes',
                               task='remotes.tasks.harvest_sources')


@celery_app.task
def harvest_sources():
    """Get a new batch of data from all sources."""
    from .models import Source
    for source in Source.objects.all():
        logger.info("Harvesting from Source: %s", source)
        harvester = source.harvester()
        for post in harvester.harvest():
            logger.info("Got new Post: %s", post)

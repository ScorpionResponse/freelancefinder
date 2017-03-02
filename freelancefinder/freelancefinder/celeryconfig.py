"""Celery bootstrap and configuration process."""
import os

from celery import Celery
from celery.utils.log import get_task_logger

import maya


logger = get_task_logger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freelancefinder.settings')

celery_app = Celery('freelancefinder')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks.py modules from all registered Django app configs.
celery_app.autodiscover_tasks()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Ensure periodic tasks are scheduled."""
    from django_celery_beat.models import IntervalSchedule, PeriodicTask
    logger.info("Configuring periodic tasks.")
    logger.debug('Sender: %s; kwargs: %s', sender, kwargs)

    schedule_4_minutes, created = IntervalSchedule.objects.get_or_create(every=4, period=IntervalSchedule.MINUTES)
    logger.debug("IntervalSchedule: %s; Created: %s", schedule_4_minutes, created)
    schedule_10_minutes, created = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.MINUTES)
    logger.debug("IntervalSchedule: %s; Created: %s", schedule_10_minutes, created)

    pertask, created = PeriodicTask.objects.get_or_create(interval=schedule_4_minutes, name="Process New Posts", task='jobs.tasks.process_new_posts')
    logger.debug("PeriodicTask: %s; Created: %s", pertask, created)
    pertask, created = PeriodicTask.objects.get_or_create(interval=schedule_4_minutes, name="Create Jobs from Posts", task='jobs.tasks.create_jobs')
    logger.debug("PeriodicTask: %s; Created: %s", pertask, created)

    pertask, created = PeriodicTask.objects.get_or_create(interval=schedule_10_minutes, name='Harvest Remotes', task='remotes.tasks.harvest_sources')
    logger.debug("PeriodicTask: %s; Created: %s", pertask, created)

    if created:
        logger.debug('Newly created harvest task, set expiry.')
        pertask.expires = maya.now().add(minutes=30).datetime()
        pertask.save()
    else:
        logger.info("Deleting old periodic task and creating a new one.")
        pertask.delete()
        PeriodicTask.objects.create(interval=schedule_10_minutes, name='Harvest Remotes', task='remotes.tasks.harvest_sources', expires=maya.now().add(minutes=30).datetime())

"""Tasks to perform periodic tasks with remotes."""

from django.conf import settings

from django_celery_beat.models import CrontabSchedule, IntervalSchedule, PeriodicTask
from celery import Celery
from celery.utils.log import get_task_logger

import maya

celery_app = Celery()
logger = get_task_logger(__name__)


@celery_app.task
def harvest_sources():
    """Get a new batch of data from all sources."""
    from .models import Source
    for source in Source.objects.all():
        logger.info("Harvesting from Source: %s", source)
        harvester = source.harvester()
        # TODO(Paul): With the frequency stuff this is kind of ugly
        frequency = None
        config_row = source.config.filter(config_key='frequency').first()
        if config_row:
            frequency = config_row.config_value
        try:
            if frequency:
                for post in harvester.harvest(frequency=frequency):
                    logger.info("Got new Post: %s", post)
                    post.save()
            else:
                for post in harvester.harvest():
                    logger.info("Got new Post: %s", post)
                    post.save()
        except Exception as harvester_exception:  # pylint: disable=broad-except
            logger.exception('Source %s harvester is broken due to: %s', source, harvester_exception)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Ensure periodic tasks are scheduled."""
    logger.info("Configuring periodic tasks.")
    logger.debug('Sender: %s; kwargs: %s', sender, kwargs)

    schedule_4_minutes, created = IntervalSchedule.objects.get_or_create(every=4, period=IntervalSchedule.MINUTES)
    logger.debug("IntervalSchedule: %s; Created: %s", schedule_4_minutes, created)
    schedule_10_minutes, created = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.MINUTES)
    logger.debug("IntervalSchedule: %s; Created: %s", schedule_10_minutes, created)
    schedule_every_hour, created = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.HOURS)
    logger.debug("IntervalSchedule: %s; Created: %s", schedule_every_hour, created)

    # UserJob Frequencies use crontab so we can control exactly when they run
    schedule_daily, created = CrontabSchedule.objects.get_or_create(minute='15', hour='4', day_of_week='*', day_of_month='*', month_of_year='*')
    logger.debug("CrontabSchedule: %s; Created: %s", schedule_daily, created)
    schedule_twice_daily, created = CrontabSchedule.objects.get_or_create(minute='20', hour='4, 16', day_of_week='*', day_of_month='*', month_of_year='*')
    logger.debug("CrontabSchedule: %s; Created: %s", schedule_twice_daily, created)
    schedule_hourly, created = CrontabSchedule.objects.get_or_create(minute='59', hour='*', day_of_week='*', day_of_month='*', month_of_year='*')
    logger.debug("CrontabSchedule: %s; Created: %s", schedule_hourly, created)

    pertask, created = PeriodicTask.objects.get_or_create(interval=schedule_every_hour, name="Send Email", task='notifications.tasks.send_notifications')
    logger.debug("PeriodicTask: %s; Created: %s", pertask, created)

    pertask, created = PeriodicTask.objects.get_or_create(interval=schedule_4_minutes, name="Process New Posts", task='jobs.tasks.process_new_posts')
    logger.debug("PeriodicTask: %s; Created: %s", pertask, created)
    pertask, created = PeriodicTask.objects.get_or_create(interval=schedule_4_minutes, name="Tag Posts", task='jobs.tasks.tag_posts')
    logger.debug("PeriodicTask: %s; Created: %s", pertask, created)
    pertask, created = PeriodicTask.objects.get_or_create(interval=schedule_4_minutes, name="Create Jobs from Posts", task='jobs.tasks.create_jobs')
    logger.debug("PeriodicTask: %s; Created: %s", pertask, created)
    pertask, created = PeriodicTask.objects.get_or_create(interval=schedule_4_minutes, name="Tag Jobs", task='jobs.tasks.tag_jobs')
    logger.debug("PeriodicTask: %s; Created: %s", pertask, created)

    pertask, created = PeriodicTask.objects.get_or_create(crontab=schedule_daily, name="Create UserJobs - Daily Users", task='jobs.tasks.create_userjobs', kwargs='{"frequency": "daily"}')
    logger.debug("PeriodicTask: %s; Created: %s", pertask, created)
    pertask, created = PeriodicTask.objects.get_or_create(crontab=schedule_twice_daily, name="Create UserJobs - Twice Daily Users", task='jobs.tasks.create_userjobs', kwargs='{"frequency": "twice_a_day"}')
    logger.debug("PeriodicTask: %s; Created: %s", pertask, created)
    pertask, created = PeriodicTask.objects.get_or_create(crontab=schedule_hourly, name="Create UserJobs - Hourly Users", task='jobs.tasks.create_userjobs', kwargs='{"frequency": "hourly"}')
    logger.debug("PeriodicTask: %s; Created: %s", pertask, created)

    pertask, created = PeriodicTask.objects.get_or_create(interval=schedule_10_minutes, name='Harvest Remotes', task='remotes.tasks.harvest_sources')
    logger.debug("PeriodicTask: %s; Created: %s", pertask, created)

    if settings.DEBUG:
        # Expire the harvest task when we're debugging
        expiry_time = maya.now().add(minutes=300).datetime()
        if created:
            logger.debug('Newly created harvest task, set expiry.')
            pertask.expires = expiry_time
            pertask.save()
        else:
            logger.info("Deleting old periodic task and creating a new one.")
            pertask.delete()
            PeriodicTask.objects.create(interval=schedule_10_minutes, name='Harvest Remotes', task='remotes.tasks.harvest_sources', expires=expiry_time)

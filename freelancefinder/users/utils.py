"""User related utilities."""

import logging
from datetime import timedelta

from django_celery_beat.models import PeriodicTask

from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils import timezone

from jobs.models import Job, UserJob

logger = logging.getLogger(__name__)


def is_in_group(user, groups):
    """
    Return a boolean indicating if a user belongs to a group.

    Usage: {% if request.user|in_group:"Group Name" %}
    """
    logger.debug('Checking whether user (%s) is in groups (%s)', user, groups)
    # TODO: User must be a User object and not just a username or id, fix that.
    groups = groups.split('|')
    groups = [g.strip() for g in groups]
    cache_key = 'in_group_{}_{}'.format(user, ''.join(groups).replace(' ', ''))

    user_is_in_group = cache.get(cache_key)
    logger.debug('Cache key %s result: %s', cache_key, user_is_in_group)
    if user_is_in_group is None:
        try:
            user_is_in_group = user.groups.filter(name__in=groups).exists()
        except AttributeError:
            user_is_in_group = False
        finally:
            cache.set(cache_key, user_is_in_group, 3600)
    return user_is_in_group


def create_userjobs_for(user):
    """Create userjobs for a specific user."""
    # TODO(Paul): Pretty sure there is a better way to do this
    today = timezone.now()
    a_week_ago = today - timedelta(days=7)

    current_userjobs = UserJob.all_objects.filter(user=user)  # pylint: disable=no-member
    query = Job.objects.exclude(userjobs__in=current_userjobs).filter(created__gte=a_week_ago)

    tags = user.profile.tags.slugs()
    if tags:
        logger.info("Got tags '%s' for user '%s'", tags, user)
        query = query.filter(tags__slug__in=tags).distinct()

    for job in query:
        logger.info("Assigning job %s to user %s", job, user)
        UserJob.objects.create(job=job, user=user)


def users_with_frequency(frequency):
    """Get users with this frequency setting."""
    return User.objects.filter(profile__refresh_frequency=frequency)


def my_next_run(user):
    """Get the time of this user's next set of jobs."""
    cache_key = "next-run-{}".format(user.username)
    estimated_next_run = cache.get(cache_key)
    if estimated_next_run:
        logger.info("Next Run got cached value user: %s, value: %s", user, estimated_next_run)
        return estimated_next_run

    refresh_frequency = user.profile.refresh_frequency
    right_now = timezone.now()

    refresh_task = PeriodicTask.objects.filter(name__icontains='Create UserJobs', kwargs__icontains=refresh_frequency).first()
    try:
        if refresh_task.last_run_at is not None:
            last_run_at = refresh_task.last_run_at
        else:
            logger.info("Tried to lookup timing for user %s with frequency %s but job had not run.", user, refresh_frequency)
            last_run_at = right_now
    except AttributeError:
        logger.warning("Tried to lookup timing for user %s with frequency %s but PeriodicTask could not be found.", user, refresh_frequency)
        last_run_at = right_now

    frequency_calculator = {
        'daily': timedelta(days=1),
        'twice_a_day': timedelta(hours=12),
        'hourly': timedelta(hours=1),
    }

    time_to_next_run = frequency_calculator[refresh_frequency]
    estimated_next_run = last_run_at + time_to_next_run
    seconds = (estimated_next_run - right_now).total_seconds()
    logger.info("Next Run caching value user: %s, value: %s, seconds: %s", user, estimated_next_run, seconds)
    cache.set(cache_key, estimated_next_run, seconds)
    return estimated_next_run

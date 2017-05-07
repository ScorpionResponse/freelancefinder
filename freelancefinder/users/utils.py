"""User related utilities."""

import logging

from django.core.cache import cache

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
    query = Job.objects.filter(userjobs__user=user, userjobs__isnull=True)

    tags = user.profile.tags
    if len(tags) > 1:
        query = query.filter(tags__in=tags)

    for job in query:
        UserJob.objects.create(job=job, user=user)

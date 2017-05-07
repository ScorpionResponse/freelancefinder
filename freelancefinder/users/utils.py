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
    # TODO(Paul): Pretty sure there is a better way to do this
    current_userjobs = UserJob.all_objects.filter(user=user)  # pylint: disable=no-member
    query = Job.objects.exclude(userjobs__in=current_userjobs)

    tags = user.profile.tags.slugs()
    if len(tags) > 1:
        query = query.filter(tags__slugs__in=tags)

    for job in query:
        logger.debug("Assigning job %s to user %s", job, user)
        UserJob.objects.create(job=job, user=user)

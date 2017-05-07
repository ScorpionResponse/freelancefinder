"""Useful cross-app fixtures."""

import pytest
from pytest_factoryboy import register
from django_factory_boy.auth import UserFactory

from django.contrib.auth.models import Group

from jobs.tests.factories import JobFactory, PostFactory, SourceFactory, TagFactory, UserJobFactory

# pylint: disable=redefined-outer-name,unused-variable


@pytest.fixture
def debug_user(django_user_model):
    """Get a user in the Debuggers group."""
    new_user = django_user_model.objects.create_user(username='debug_user', email='debug@example.com')
    group, created = Group.objects.get_or_create(name='Debuggers')
    new_user.groups.add(group)
    new_user.save()
    return new_user


@pytest.fixture
def debug_group_client(client, debug_user):
    """Get a client in the Debuggers group."""
    client.force_login(debug_user)
    return client


@pytest.fixture
def admin_user(django_user_model):
    """Get a user in the Administrators group."""
    new_user = django_user_model.objects.create_user(username='admin_user', email='admin@example.com')
    group, created = Group.objects.get_or_create(name='Administrators')
    new_user.groups.add(group)
    new_user.save()
    return new_user


@pytest.fixture
def admin_group_client(client, admin_user):
    """Get a client in the Administrators group."""
    client.force_login(admin_user)
    return client


@pytest.fixture
def paid_user(django_user_model):
    """Get a user in the Paid group."""
    new_user = django_user_model.objects.create_user(username='paid_user', email='paid@example.com')
    group, created = Group.objects.get_or_create(name='Paid')
    new_user.groups.add(group)
    new_user.save()
    return new_user


@pytest.fixture
def paid_group_client(client, paid_user):
    """Get a client in the Paid group."""
    client.force_login(paid_user)
    return client


@pytest.fixture
def authed_user(django_user_model):
    """Get a logged in user."""
    new_user = django_user_model.objects.create_user(username='joe_user', email='joe@example.com')
    return new_user


@pytest.fixture
def authed_client(client, authed_user):
    """Get a client that is logged in."""
    client.force_login(authed_user)
    return client


register(TagFactory)
register(JobFactory)
register(PostFactory)
register(SourceFactory)
register(UserJobFactory)
register(UserFactory)

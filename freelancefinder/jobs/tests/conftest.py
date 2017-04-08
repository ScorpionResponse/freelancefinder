"""Fixtures to create models in jobs app."""

import pytest
from pytest_factoryboy import register

from django.contrib.auth.models import Group

from .factories import JobFactory, PostFactory, FreelancerFactory, SourceFactory, TagFactory


register(TagFactory)
register(JobFactory)
register(PostFactory)
register(FreelancerFactory)
register(SourceFactory)


@pytest.fixture(scope="function")
def admin_group_client(client, django_user_model):
    """Get a client in the Administrators group."""
    new_user = django_user_model.objects.create_user(username='admin_user', email='admin@example.com')
    group, created = Group.objects.get_or_create(name='Administrators')
    new_user.groups.add(group)
    new_user.save()

    client.force_login(new_user)
    return client


@pytest.fixture(scope="function")
def paid_group_client(client, django_user_model):
    """Get a client in the Paid group."""
    new_user = django_user_model.objects.create_user(username='paid_user', email='paid@example.com')
    group, created = Group.objects.get_or_create(name='Paid')
    new_user.groups.add(group)
    new_user.save()

    client.force_login(new_user)
    return client


@pytest.fixture(scope="function")
def authed_client(client, django_user_model):
    """Get a client that is logged in."""
    new_user = django_user_model.objects.create_user(username='joe_user', email='joe@example.com')

    client.force_login(new_user)
    return client

"""Tests related to users and accounts."""

from django.contrib.auth.models import Group


def test_login_changes(client, admin_user):
    """Test that the page changes on login."""
    client.force_login(admin_user)
    response = client.get('/')
    assert 'AUTH:YES' in response.content.decode('utf-8')


def test_no_group(client, django_user_model):
    """Test that page changes based on Group affiliation - no group."""
    new_user = django_user_model.objects.create_user(username='joe', email='joe@example.com')
    client.force_login(new_user)
    response = client.get('/')
    assert '>Jobs<' in response.content.decode('utf-8')


def test_admin_group(client, django_user_model):
    """Test that page changes based on Group affiliation - Administrators group."""
    new_user = django_user_model.objects.create_user(username='admin_user', email='admin@example.com')
    group, created = Group.objects.get_or_create(name='Administrators')
    new_user.groups.add(group)
    new_user.save()
    assert not created

    client.force_login(new_user)
    response = client.get('/')
    assert '>Posts<' in response.content.decode('utf-8')


def test_debug_group(client, django_user_model):
    """Test that page changes based on Group affiliation - Debuggers group."""
    new_user = django_user_model.objects.create_user(username='debug_user', email='debug@example.com')
    group, created = Group.objects.get_or_create(name='Debuggers')
    new_user.groups.add(group)
    new_user.save()
    assert not created

    client.force_login(new_user)
    response = client.get('/')
    assert '>Sources<' in response.content.decode('utf-8')


def test_anonymous(client):
    """Test that the page shows anonymous for non-logged in user."""
    response = client.get('/')
    assert 'AUTH:NO' in response.content.decode('utf-8')
    assert str(response.context['user']) == 'AnonymousUser'


def test_user_creates_profile(django_user_model):
    """Test that creating a user creates the associated profile."""
    new_user = django_user_model.objects.create(email='test@example.com')
    assert new_user is not None
    assert new_user.profile is not None
    assert 'America' in str(new_user.profile)
    assert new_user.profile.custom_timezone == 'America/New_York'

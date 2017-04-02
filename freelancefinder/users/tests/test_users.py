"""Tests related to users and accounts."""


def test_login_changes(client, admin_user):
    """Test that the page changes on login."""
    client.force_login(admin_user)
    response = client.get('/')
    assert 'AUTH:YES' in response.content.decode('utf-8')


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

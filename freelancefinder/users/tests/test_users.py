"""Tests related to users and accounts."""


def test_login_changes(authed_client):
    """Test that the page changes when logged in."""
    response = authed_client.get('/')
    assert 'AUTH:YES' in response.content.decode('utf-8')


def test_no_group(authed_client):
    """Test that page changes based on Group affiliation - no group."""
    response = authed_client.get('/')
    assert '>My Opportunities<' in response.content.decode('utf-8')


def test_admin_group(admin_group_client):
    """Test that page changes based on Group affiliation - Administrators group."""
    response = admin_group_client.get('/')
    assert '>Posts<' in response.content.decode('utf-8')


def test_debug_group(debug_group_client):
    """Test that page changes based on Group affiliation - Debuggers group."""
    response = debug_group_client.get('/')
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

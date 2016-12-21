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

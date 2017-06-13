"""Tests for notifications."""


def test_message_url_nologin(client, message):
    """Test message factory url requires login."""
    response = client.get('/notifications/{}'.format(message.url))
    print(response.content)
    assert response.status_code == 302


def test_message_url(authed_client, message):
    """Test message factory url renders something."""
    response = authed_client.get('/notifications/{}'.format(message.url))
    assert response.status_code == 200

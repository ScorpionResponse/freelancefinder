"""Test the Timezone middleware."""

import pytz

from django.contrib.auth.models import AnonymousUser
from django.utils.timezone import get_current_timezone

from ..middleware.timezone import user_timezone


def get_response_method(thing):
    """Do nothing."""
    return thing


def test_unauthed_user_uses_utc(rf):
    """AnonymousUsers should have timezone UTC."""

    timezone_middleware = user_timezone(get_response_method)
    request = rf.get('/')
    request.user = AnonymousUser()
    response = timezone_middleware(request)
    current_timezone = get_current_timezone()
    assert response is not None
    assert current_timezone == pytz.timezone('UTC')


def test_authed_user_uses_profile(rf, django_user_model):
    """Test Timezone setting on a real user."""

    new_user = django_user_model.objects.create(email='test@example.com')
    new_user.profile.custom_timezone = 'US/Eastern'

    timezone_middleware = user_timezone(get_response_method)
    request = rf.get('/')
    request.user = new_user
    response = timezone_middleware(request)
    current_timezone = get_current_timezone()
    assert response is not None
    assert current_timezone != pytz.timezone('UTC')
    assert current_timezone == pytz.timezone('US/Eastern')

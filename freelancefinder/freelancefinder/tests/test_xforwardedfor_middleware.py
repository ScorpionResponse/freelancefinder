"""Test the X-Forwarded-For middleware."""

from ..middleware.xforwardedfor import xforwardedfor


def get_response_method(thing):
    """Do nothing."""
    return thing


def test_setting_correctly(rf):
    """Override REMOTE_ADDR if HTTP_X_FORWARDED_FOR is present."""
    request = rf.get('/')
    request.META['REMOTE_ADDR'] = '192.168.1.1'
    request.META['HTTP_X_FORWARDED_FOR'] = '192.168.1.2'

    xforwardedfor_middleware = xforwardedfor(get_response_method)
    response = xforwardedfor_middleware(request)

    assert response is not None
    assert request.META['REMOTE_ADDR'] == '192.168.1.2'


def test_nothing_on_missing_value(rf):
    """Don't override REMOTE_ADDR if HTTP_X_FORWARDED_FOR is not present."""
    request = rf.get('/')
    request.META['REMOTE_ADDR'] = '192.168.1.1'

    xforwardedfor_middleware = xforwardedfor(get_response_method)
    response = xforwardedfor_middleware(request)

    assert response is not None
    assert request.META['REMOTE_ADDR'] == '192.168.1.1'

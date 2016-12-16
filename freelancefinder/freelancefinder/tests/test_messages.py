"""
Test for flash messages.

Verifies that all types of flash messages display to the user appropriately.
"""
import pytest

from django.contrib.messages import constants
from django.contrib.messages.storage.fallback import FallbackStorage

from freelancefinder.views import IndexPageView


def _add_message(request, lvl):
    """Helper to add a message to a requestfactory."""
    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    messages.add(constants.DEFAULT_LEVELS[lvl], "LVL-{}-MESSAGE".format(lvl))
    setattr(request, '_messages', messages)


@pytest.fixture(params=['ERROR', 'WARNING', 'INFO', 'SUCCESS'])
def level(request):
    """Return the message levels as a fixture."""
    yield request.param


def test_message(rf, level):
    """Test a single message type and ensure it displays."""

    request = rf.get('/')
    _add_message(request, level)
    response = IndexPageView.as_view()(request)

    level_id = constants.DEFAULT_LEVELS[level]
    tag = constants.DEFAULT_TAGS[level_id]

    assert response.status_code == 200
    assert "alert-{}".format(tag) in response.rendered_content
    assert "LVL-{}-MESSAGE".format(level) in response.rendered_content

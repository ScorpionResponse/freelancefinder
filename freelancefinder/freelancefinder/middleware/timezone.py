"""Timezone setting middleware."""

import pytz

from django.utils import timezone


def user_timezone(get_response):
    """Middleware to engage the appropriate timezone."""
    def middleware(request):
        """If the user is logged in, use their profile, otherwise guess."""

        tzone = None
        if request.user.is_authenticated():
            tzone = request.user.profile.custom_timezone

        # TODO(Paul): Guess Timezone

        if tzone:
            timezone.activate(pytz.timezone(tzone))
        else:
            timezone.deactivate()

        response = get_response(request)
        return response

    return middleware

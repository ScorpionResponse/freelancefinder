"""X-Forwarded-For processing middleware."""


class XForwardedForMiddleware(object):
    """Middleware to add appropriate REMOTE_ADDR header."""

    def process_request(self, request):
        """Insert appropriate REMOTE_ADDR header."""

        if 'REMOTE_ADDR' not in request.META and 'X_FORWARDED_FOR' in request.META:
            request.META['REMOTE_ADDR'] = request.META['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()
        return None

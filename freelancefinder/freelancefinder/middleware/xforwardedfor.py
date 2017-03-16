"""X-Forwarded-For processing middleware."""


class XForwardedForMiddleware(object):
    """Middleware to add appropriate REMOTE_ADDR header."""

    def __init__(self, get_response):
        """Init the middleware."""
        self.get_response = get_response

    def __call__(self, request):
        """Call the middleware."""

        if 'REMOTE_ADDR' not in request.META and 'X_FORWARDED_FOR' in request.META:
            request.META['REMOTE_ADDR'] = request.META['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()

        response = self.get_response(request)

        return response

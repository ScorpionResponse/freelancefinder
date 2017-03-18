"""X-Forwarded-For processing middleware."""


def xforwardedfor(get_response):
    """Middleware to add appropriate REMOTE_ADDR header."""
    def middleware(request):
        """Set the REMOTE_ADDR to the X-Forwarded-For value."""
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            request.META['REMOTE_ADDR'] = request.META['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()
        response = get_response(request)
        return response

    return middleware

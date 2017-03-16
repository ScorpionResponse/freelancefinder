"""X-Forwarded-For processing middleware."""
import logging

logger = logging.getLogger(__name__)


class XForwardedForMiddleware(object):
    """Middleware to add appropriate REMOTE_ADDR header."""

    def __init__(self, get_response):
        """Init the middleware."""
        self.get_response = get_response

    def __call__(self, request):
        """Call the middleware."""

        logger.debug("X-Forwarded-For middleware: %s", request.META)
        if 'REMOTE_ADDR' not in request.META and 'X_FORWARDED_FOR' in request.META:
            logger.debug("X-Forwarded-For middleware setting REMOTE ADDR to: %s", request.META['X_FORWARDED_FOR'])
            request.META['REMOTE_ADDR'] = request.META['X_FORWARDED_FOR'].split(",")[0].strip()

        response = self.get_response(request)

        return response

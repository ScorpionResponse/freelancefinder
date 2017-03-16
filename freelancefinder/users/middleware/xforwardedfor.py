"""X-Forwarded-For processing middleware."""
import logging

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class XForwardedForMiddleware(MiddlewareMixin):
    """Middleware to add appropriate REMOTE_ADDR header."""

    def __init__(self, get_response):
        """Init the middleware."""
        self.get_response = get_response
        logger.info("initializing x-forwarded-for middleware.")

    def process_request(self, request):
        """Process request, add header."""
        logger.info("X-Forwarded-For middleware: %s", request.META)
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            logger.info("X-Forwarded-For middleware setting REMOTE ADDR to: %s", request.META['HTTP_X_FORWARDED_FOR'])
            request.META['REMOTE_ADDR'] = request.META['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()
        return None

"""Basic import for freelancefinder app."""

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celeryconfig import celery_app

__all__ = ('celery_app',)

__version__ = '1.2.1'
VERSION = __version__

"""Tasks to handle sending notifications."""

from celery import Celery
from celery.utils.log import get_task_logger

celery_app = Celery()
logger = get_task_logger(__name__)


@celery_app.task
def send_notifications():
    """Send all pending notifications."""
    from .models import NotificationHistory
    for message in NotificationHistory.objects.filter(sent=False):
        logger.info("Sending message: %s", message)
        message.send()

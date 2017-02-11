"""Celery bootstrap and configuration process."""
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freelancefinder.settings')

celery_app = Celery('freelancefinder')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks.py modules from all registered Django app configs.
celery_app.autodiscover_tasks()

# Configure periodic tasks
celery_app.conf.beat_schedule = {
    'harvest_every_10_minutes': {
        'task': 'remotes.tasks.harvest_sources',
        'schedule': crontab(minute='*/10'),
    },
}

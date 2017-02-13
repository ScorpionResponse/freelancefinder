"""Celery bootstrap and configuration process."""
import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freelancefinder.settings')

celery_app = Celery('freelancefinder')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks.py modules from all registered Django app configs.
celery_app.autodiscover_tasks()

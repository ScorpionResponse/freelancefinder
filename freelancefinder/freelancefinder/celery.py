"""Celery bootstrap and configuration process."""
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freelancefinder.settings')

app = Celery('freelancefinder')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks.py modules from all registered Django app configs.
app.autodiscover_tasks()

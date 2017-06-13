"""
URLs for the notifications application.

The base URL for these is /notifications/.
"""
from django.conf.urls import url

from .views import NotificationView

urlpatterns = [
    url(r'^(?P<url>.*/)$', NotificationView.as_view(), name="notification"),
]

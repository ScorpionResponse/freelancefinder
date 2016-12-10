"""
URLs for the users application.

The base URL for these is /users/.
"""
from django.conf.urls import url

from .views import UserProfileView

urlpatterns = [
    url(r'^$', UserProfileView.as_view(), name="user-profile"),
]

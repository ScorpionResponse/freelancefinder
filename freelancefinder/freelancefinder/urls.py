"""
Main URL configuration for the FreelanceFinder application.

The base URL for this is /
"""
from django.conf.urls import url, include
from django.contrib import admin

from .views import IndexPageView

admin.autodiscover()

urlpatterns = [
    url(r'^$', IndexPageView.as_view(), name='index'),
    url(r'^$', IndexPageView.as_view(), name='all-links'),
    url(r'^jobs/', include('jobs.urls')),
    url(r'^remotes/', include('remotes.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^accounts/', include('authtools.urls')),
    url(r'^freelance_admin/', admin.site.urls),
]

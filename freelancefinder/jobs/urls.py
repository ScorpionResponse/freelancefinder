"""
Configure urls for the jobs app.

The default base for these urls is /jobs/
"""
from django.conf.urls import url

from .views import (JobListView, JobDetailView, PostListView, PostActionView, UserJobListView)

urlpatterns = [
    url(r'^my-opportunities/$', UserJobListView.as_view(), name="userjob-list"),
    url(r'^job-list/$', JobListView.as_view(), name="job-list"),
    url(r'^job/(?P<pk>\d+)/$', JobDetailView.as_view(), name="job-detail"),
    url(r'^post-list/$', PostListView.as_view(), name="post-list"),
    url(r'^post-action/$', PostActionView.as_view(), name="post-action"),
]

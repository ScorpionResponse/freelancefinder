"""
Configure urls for the jobs app.

The default base for these urls is /jobs/
"""
from django.conf.urls import url

from .views import (JobListView, JobDetailView, PostListView, PostActionView,
                    UserJobListView, UserJobActionView, UserJobRedirectView)

urlpatterns = [
    url(r'^my-opportunities/$', UserJobRedirectView.as_view(), name="userjob-list"),
    url(r'^my-opportunities/(?P<date>\d{4}-\d{2}-\d{2})/$', UserJobListView.as_view(), name="userjob-list"),
    url(r'^my-opportunities/action/$', UserJobActionView.as_view(), name="userjob-action"),
    url(r'^job-list/$', JobListView.as_view(), name="job-list"),
    url(r'^job/(?P<pk>\d+)/$', JobDetailView.as_view(), name="job-detail"),
    url(r'^post-list/$', PostListView.as_view(), name="post-list"),
    url(r'^post-action/$', PostActionView.as_view(), name="post-action"),
]

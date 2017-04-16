"""
Configure urls for the jobs app.

The default base for these urls is /jobs/
"""
from django.conf.urls import url

from .views import (JobListView, JobDetailView, PostListView, PostActionView,
                    FreelancerListView, FreelancerDetailView)

urlpatterns = [
    url(r'^job-list/$', JobListView.as_view(), name="job-list"),
    url(r'^job/(?P<pk>\d+)/$', JobDetailView.as_view(), name="job-detail"),
    url(r'^freelancer-list/$', FreelancerListView.as_view(), name="freelancer-list"),
    url(r'^freelancer/(?P<pk>\d+)/$', FreelancerDetailView.as_view(), name="freelancer-detail"),
    url(r'^post-list/$', PostListView.as_view(), name="post-list"),
    url(r'^post-list/$', PostActionView.as_view(), name="post-action"),
]

"""
Configure urls for the jobs app.

The default base for these urls is /jobs/
"""
from django.conf.urls import url

from .views import JobListView, JobDetailView, PostListView

urlpatterns = [
    url(r'^job-list/$', JobListView.as_view(), name="job-list"),
    url(r'^job/(?P<pk>\d+)/$', JobDetailView.as_view(), name="job-detail"),
    url(r'^post-list/$', PostListView.as_view(), name="post-list"),
]

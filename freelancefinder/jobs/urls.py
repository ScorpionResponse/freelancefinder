from django.conf.urls import url

from .views import JobListView, PostListView

urlpatterns = [
    url(r'^job-list/$', JobListView.as_view(), name="job-list"),
    url(r'^post-list/$', PostListView.as_view(), name="post-list"),
]

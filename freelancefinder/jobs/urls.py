from django.conf.urls import url

from .views import JobListView, PostListView

urlpatterns = [
    url(r'^$', JobListView.as_view(), name="all-jobs"),
]

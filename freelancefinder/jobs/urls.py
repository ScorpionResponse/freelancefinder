from django.conf.urls import url

from .views import AllJobsView

urlpatterns = [
    url(r'^$', AllJobsView.as_view(), name="all-jobs"),
]

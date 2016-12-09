from django.conf.urls import url

from .views import SourceListView

urlpatterns = [
    url(r'^source-list/$', SourceListView.as_view(), name="source-list"),
]

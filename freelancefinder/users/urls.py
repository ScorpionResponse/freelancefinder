from django.conf.urls import url

from .views import UserProfileView

urlpatterns = [
    url(r'^$', UserProfileView.as_view(), name="user-profile"),
]
from django.conf.urls import url, include
from django.contrib import admin

from .views import IndexPageView

admin.autodiscover()

urlpatterns = [
    url(r'^$', IndexPageView.as_view(), name='index'),
    url(r'^/$', IndexPageView.as_view(), name='all-links'),
    url(r'^users/', include('users.urls')),
    url(r'^freelance_admin/', admin.site.urls),
]

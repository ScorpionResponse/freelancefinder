from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from .views import IndexPageView

urlpatterns = [
    url(r'^$', IndexPageView.as_view(), name='index'),
    url(r'^user/', include('users.urls')),
    url(r'^freelance_admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

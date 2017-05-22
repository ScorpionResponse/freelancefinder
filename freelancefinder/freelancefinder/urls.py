"""
Main URL configuration for the FreelanceFinder application.

The base URL for this is /
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from contact_form.views import ContactFormView

from .forms import CrispyContactForm
from .views import IndexPageView, AcceptPaymentView

admin.autodiscover()

urlpatterns = [
    url(r'^$', IndexPageView.as_view(), name='index'),
    url(r'^jobs/', include('jobs.urls')),
    url(r'^remotes/', include('remotes.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^contact/$', ContactFormView.as_view(form_class=CrispyContactForm), name='contact_form'),
    url(r'^contact/sent/$', TemplateView.as_view(template_name='contact_form/contact_form_sent.html'), name='contact_form_sent'),
    url(r'^accept-payment/$', AcceptPaymentView.as_view(), name='accept-payment'),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^freelance_admin/', admin.site.urls),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots.txt'),
    url(r'^humans\.txt$', TemplateView.as_view(template_name='humans.txt', content_type='text/plain'), name='humans.txt'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

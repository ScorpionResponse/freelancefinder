"""Views for Notifications."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.template import Context, Template
from django.views.generic import TemplateView

from .models import Message


class NotificationView(LoginRequiredMixin, TemplateView):
    """Render a notification at a URL."""

    template_name = 'notifications/base.html'

    def get_context_data(self, **kwargs):
        """Add the same context as when rendering emails."""
        context = super(NotificationView, self).get_context_data(**kwargs)
        message = get_object_or_404(Message, url=kwargs['url'])

        subject_template = Template(message.subject)
        subject_context = Context({'user': self.request.user, 'message': message})
        subject = subject_template.render(subject_context)

        email_template = Template(message.email_body)
        email_context = Context({'user': self.request.user, 'message': message})
        email_message = email_template.render(email_context)

        # These must match the fields present in
        # notifications.models.Notification.get_email_message
        context['user'] = self.request.user
        context['message'] = message
        context['subject'] = subject
        context['email_message'] = email_message
        return context

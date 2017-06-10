"""Define the notification type and track sent notifications."""

import logging
from smtplib import SMTPException

from future.utils import python_2_unicode_compatible
from model_utils import Choices
from model_utils.fields import MonitorField
from model_utils.models import TimeStampedModel

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.template import Context, Template
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Message(models.Model):
    """Define a message to the user."""

    url = models.CharField(max_length=100, db_index=True, unique=True)
    subject = models.CharField(max_length=300)
    email_body = models.TextField(blank=True)
    slack_body = models.TextField(blank=True)

    def __str__(self):
        """Representation for a Message."""
        return u"<Message ID:{}; URL:{}; Subject:{}>".format(self.pk, self.url, self.subject)


@python_2_unicode_compatible
class Notification(models.Model):
    """Define a pending notification."""

    TYPES = Choices('signup', 'welcome_package', 'one_time', 'expiration')

    notification_type = models.CharField(choices=TYPES, default=TYPES.one_time, max_length=50)
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, related_name="notifications")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="notifications")

    def __str__(self):
        """Representation for a Notification."""
        return u"<Notification ID:{}; Type:{}; User: {}; Message:{}>".format(self.pk, self.notification_type, self.user, self.message)

    def get_email_message(self):
        """Render the templates to create the message."""
        subject_template = Template(self.message.subject)
        subject_context = Context({'user': self.user, 'message': self.message})
        subject = subject_template.render(subject_context)

        email_template = Template(self.message.email_body)
        email_context = Context({'user': self.user, 'message': self.message})
        email_message = email_template.render(email_context)

        html_template = Template('notifications/base.html')
        html_context = Context({'message': self.message, 'email_message': email_message})
        html_message = html_template.render(html_context)

        txt_message = strip_tags(html_message)

        return (subject, html_message, txt_message)

    def schedule_for_all_users(self):
        """Send this notification to all users."""
        if self.user:
            self.history.create(user=self.user)
        else:
            for user in User.objects.filter(groups__name="Paid"):
                self.history.create(user=user)


@python_2_unicode_compatible
class NotificationHistory(TimeStampedModel):
    """Tracks whether each user has received a notification."""

    # Added by TimeStampedModel
    # created = models.DateTimeField(auto_now_add=True)
    # modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_history")
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="history")
    sent = models.BooleanField(default=False)
    sent_at = MonitorField(monitor='sent', when=[True])

    def __str__(self):
        """Representation for a NotificationHistory."""
        return u"<NotificationHistory ID:{}; User:{}; Notification:{}; Sent:{}>".format(self.pk, self.user, self.notification, self.sent)

    def send(self):
        """Send a notification."""
        (subject, html_message, txt_message) = self.notification.get_email_message()
        try:
            send_mail(
                subject=subject,
                message=txt_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.user.email],
                html_message=html_message
            )
            self.sent = True
            self.save()
        except SMTPException as smtpe:
            logger.exception("Error sending notification: %s; Error: %s", self, smtpe)

    class Meta:
        """Meta info for history."""

        unique_together = ('user', 'notification')

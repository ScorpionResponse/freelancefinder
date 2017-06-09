"""Define the notification type and track sent notifications."""

from future.utils import python_2_unicode_compatible
from model_utils import Choices
from model_utils.fields import MonitorField
from model_utils.models import TimeStampedModel

from django.db import models


@python_2_unicode_compatible
class Message(models.Model):
    """Define a message to the user."""

    url = models.CharField(max_length=100, db_index=True, unique=True)
    subject = models.CharField(max_length=300)
    email_body = models.TextField(blank=True)
    slack_body = models.TextField(blank=True)

    def __str__(self):
        return u"<Message ID:{}; URL:{}; Subject:{}>".format(self.pk, self.url, self.subject)


@python_2_unicode_compatible
class Notification(models.Model):
    """Define an available notification."""

    TYPES = Choices('signup', 'welcome_package', 'one_time', 'expiration')

    notification_type = models.CharField(choices=TYPES, default=TYPES.one_time, max_length=50)
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, related_name="notifications")

    def __str__(self):
        return u"<Notification ID:{}; Type:{}; Email:{}; Slack:{}>".format(self.pk, self.notification_type, self.email_message, self.slack_message)


@python_2_unicode_compatible
class NotificationHistory(TimeStampedModel):
    """Tracks whether each user has received a notification."""

    # Added by TimeStampedModel
    # created = models.DateTimeField(auto_now_add=True)
    # modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    sent = models.BooleanField(default=False)
    sent_at = MonitorField(monitor='sent', when=[True])

    def __str__(self):
        return u"<NotificationHistory ID:{}; User:{}; Notification:{}; Sent:{}>".format(self.pk, self.user, self.notification, self.sent)

    class Meta:
        """Meta info for history."""

        unique_together = ('user', 'notification')

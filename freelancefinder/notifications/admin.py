"""Admin site configuration for the notifications app."""
import logging

from django.contrib import admin
from django.contrib import messages

from .models import Message, Notification, NotificationHistory

logger = logging.getLogger(__name__)


def send_to_all_users(modeladmin, request, queryset):
    """Send this message to all users."""
    logger.debug('MA: %s, request: %s', modeladmin, request)
    logger.info("Scheduling notification for all users: %s", queryset)
    if len(queryset) > 1:
        messages.warning(request, 'Not scheduling multiple notifications')
        return
    notification = queryset.get()
    notification.schedule_for_all_users()
    messages.success(request, "Notification {} scheduled for all users.".format(notification))


def resend_notifications(modeladmin, request, queryset):
    """Resend already sent notifications."""
    logger.debug('MA: %s, request: %s', modeladmin, request)
    resent_count = 0
    for obj in queryset:
        if obj.sent:
            obj.sent = False
            obj.save()
            resent_count += 1
    messages.success(request, "Resending {} notifications".format(resent_count))


send_to_all_users.short_description = "Send this notification to all users"
resend_notifications.short_description = "Resend notifications"


class MessageAdmin(admin.ModelAdmin):
    """Admin for the Message model."""

    model = Message

    # List fields
    list_display = ('url', 'subject')
    search_display = ('url', 'subject')

    # Detail screen
    fields = ('url', 'subject', 'email_body', 'slack_body')


class NotificationAdmin(admin.ModelAdmin):
    """Admin for the Notification model."""

    model = Notification
    actions = [send_to_all_users]

    # List fields
    list_display = ('notification_type', 'message', 'user')
    search_display = ('message', 'user')
    list_filter = ('notification_type',)

    # Detail screen
    fields = ('notification_type', 'message', 'user')


class NotificationHistoryAdmin(admin.ModelAdmin):
    """Admin for the NotificationHistory model."""

    model = NotificationHistory
    actions = [resend_notifications]

    # List fields
    list_display = ('user', 'notification', 'sent', 'sent_at', 'created', 'modified')
    search_fields = ('user', 'notification')
    list_filter = ('sent', 'user', 'notification')

    # Detail screen
    fields = ('user', 'notification', 'sent', 'sent_at', 'created', 'modified')
    readonly_fields = ('sent_at', 'created', 'modified')


admin.site.register(Message, MessageAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(NotificationHistory, NotificationHistoryAdmin)

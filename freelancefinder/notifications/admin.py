"""Admin site configuration for the notifications app."""
from django.contrib import admin

from .models import Message, Notification, NotificationHistory


class MessageAdmin(admin.ModelAdmin):
    """Admin for the Message model."""

    model = Message


class NotificationAdmin(admin.ModelAdmin):
    """Admin for the Notification model."""

    model = Notification


class NotificationHistoryAdmin(admin.ModelAdmin):
    """Admin for the NotificationHistory model."""

    model = NotificationHistory


admin.site.register(Message, MessageAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(NotificationHistory, NotificationHistoryAdmin)

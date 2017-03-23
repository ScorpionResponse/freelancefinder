"""Admin site configuration for the users app."""

from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    """The Profile Admin."""

    model = Profile
    list_display = ('user', 'custom_timezone')


admin.site.register(Profile, ProfileAdmin)

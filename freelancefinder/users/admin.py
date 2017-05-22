"""Admin site configuration for the users app."""

from django.contrib import admin

from .models import Profile, Account


class ProfileAdmin(admin.ModelAdmin):
    """The Profile Admin."""

    model = Profile
    list_display = ('user', 'custom_timezone', 'refresh_frequency', 'tag_list')

    def get_queryset(self, request):
        """Prefetch the tags data to make this more efficient."""
        return super(ProfileAdmin, self).get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):  # pylint: disable=no-self-use
        """Concatenate all tags for each profile."""
        return u", ".join(o.name for o in obj.tags.all())


class AccountAdmin(admin.ModelAdmin):
    """The Account admin."""

    model = Account
    list_display = ('user', 'stripe_customer_id', 'stripe_subscription_id', 'stripe_subscription_created', 'subscription')
    list_filter = ('subscription',)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Account, AccountAdmin)

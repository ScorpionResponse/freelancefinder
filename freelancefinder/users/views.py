"""Simple views for users info."""

from django.views.generic.base import TemplateView


class UserProfileView(TemplateView):
    """Show current user profile."""

    template_name = "users/profile.html"

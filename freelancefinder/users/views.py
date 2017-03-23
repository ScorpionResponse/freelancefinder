"""Simple views for users info."""

from braces.views import LoginRequiredMixin

from django.views.generic.base import TemplateView


class UserProfileView(TemplateView, LoginRequiredMixin):
    """Show current user profile."""

    template_name = "users/profile.html"

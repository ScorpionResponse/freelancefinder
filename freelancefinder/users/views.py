"""Simple views for users info."""

from braces.views import LoginRequiredMixin

from django.views.generic.base import TemplateView


class UserProfileView(LoginRequiredMixin, TemplateView):
    """Show current user profile."""

    template_name = "users/profile.html"

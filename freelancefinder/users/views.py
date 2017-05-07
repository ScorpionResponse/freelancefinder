"""Simple views for users info."""

import logging

from braces.views import LoginRequiredMixin

from django.views.generic.edit import FormView

from .forms import ProfileForm

logger = logging.getLogger(__name__)


class UserProfileView(LoginRequiredMixin, FormView):
    """Show current user profile."""

    template_name = "users/profile.html"
    form_class = ProfileForm

    def get_context_data(self, **kwargs):
        """Add user to kwargs."""
        kwargs = super(UserProfileView, self).get_context_data(**kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def get_form_kwargs(self):
        """Add user to kwargs."""
        kwargs = super(UserProfileView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

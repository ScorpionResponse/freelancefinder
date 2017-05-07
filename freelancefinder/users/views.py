"""Simple views for users info."""

import logging

from braces.views import LoginRequiredMixin

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import ProfileForm

logger = logging.getLogger(__name__)


class UserProfileView(LoginRequiredMixin, FormView):
    """Show current user profile."""

    template_name = "users/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy('userjob-list')

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

    def form_valid(self, form):
        """Save form and return."""
        form.save()
        messages.success(self.request, "Profile changes saved.")
        return super(UserProfileView, self).form_valid(form)

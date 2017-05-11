"""Simple views for users info."""

import logging

from braces.views import LoginRequiredMixin

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from .forms import ProfileForm
from .models import Profile
from .utils import my_next_run

logger = logging.getLogger(__name__)


class UserProfileView(LoginRequiredMixin, UpdateView):
    """Show current user profile."""

    template_name = "users/profile.html"
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('userjob-list')

    def get_object(self, queryset=None):
        """Use the logged in user's profile."""
        return self.request.user.profile

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        form.save()
        messages.success(self.request, "Profile changes saved.")
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['my_next_run'] = my_next_run(self.request.user)
        return context

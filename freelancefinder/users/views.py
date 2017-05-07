"""Simple views for users info."""

import logging

from braces.views import LoginRequiredMixin

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from .forms import ProfileForm
from .models import Profile

logger = logging.getLogger(__name__)


class UserProfileView(LoginRequiredMixin, UpdateView):
    """Show current user profile."""

    template_name = "users/profile.html"
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('userjob-list')

    def get_object(self, queryset=None):
        return self.request.user

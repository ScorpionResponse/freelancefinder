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
    success_url = '/'

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

class BullShit(FormView):
    def get(self, request, *args, **kwargs):
        """Handles GET requests and instantiates a blank version of the form."""
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        logger.info("Form: %s", form)
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

"""Forms for users."""

import logging

from django import forms

from .models import Profile

logger = logging.getLogger(__name__)


class ProfileForm(forms.ModelForm):
    """Form for setting user's profile info."""
    class Meta:
        model = Profile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """Pop the user out of kwargs."""
        self.user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        logger.info("initializing form: %s", self)

    def save(self, commit=False):
        """Make sure we save the user."""
        profile = super(ProfileForm, self).save(commit=commit)
        if self.user:
            profile.user = self.user
        profile.save()
        return profile

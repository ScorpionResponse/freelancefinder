"""Forms for users."""

import logging

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms

from .models import Profile

logger = logging.getLogger(__name__)


class ProfileForm(forms.ModelForm):
    """Form for setting user's profile info."""

    class Meta:
        """ProfileForm config info."""

        model = Profile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """Pop the user out of kwargs."""
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Save'))

class Bullshit():
    def save(self, commit=True):
        """Make sure we save the user."""
        self.instance = self.user.profile
        return super(ProfileForm, self).save(commit=commit)

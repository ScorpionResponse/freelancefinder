"""Forms for users."""

import logging

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder
from django_select2.forms import Select2Widget
from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget

from django import forms
from django.urls.base import reverse

from .models import Profile

logger = logging.getLogger(__name__)


class ProfileForm(forms.ModelForm):
    """Form for setting user's profile info."""

    tags = TagField(required=True, widget=LabelWidget, help_text="Only jobs with these tags will be shown to you.")

    class Meta:
        """ProfileForm config info."""

        model = Profile
        exclude = ('user',)
        widgets = {
            'custom_timezone': Select2Widget,
        }

    def __init__(self, *args, **kwargs):
        """Add Crispy Forms helpers."""
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Save'))


class CustomSignupForm(forms.ModelForm):
    """Force the user to input tags on signup."""

    tags = TagField(required=True, widget=LabelWidget, help_text="Only jobs with these tags will be shown to you.")

    class Meta:
        """CustomSignupForm config info."""

        model = Profile
        fields = ('tags',)

    def __init__(self, *args, **kwargs):
        """Create a pretty crispy form."""
        self.helper = FormHelper()
        self.helper.form_action = reverse('account_signup')
        self.helper.form_id = 'signup_form'
        self.helper.form_class = 'signup'
        self.helper.layout = Layout(
            Fieldset(
                'Account Details',
                'username',
                'email',
                'password1',
                'password2'
            ),
            Fieldset(
                'My Profile',
                'tags'
            ),
            ButtonHolder(
                Submit('submit', 'Sign Up &raquo;')
            )
        )
        super(CustomSignupForm, self).__init__(*args, **kwargs)

    def signup(self, request, user):
        """Provide custom signup method."""
        logger.info("User Signup: %s; request: %s", user, request)
        user.profile.tags = self.cleaned_data['tags']
        user.profile.save()
        return super(CustomSignupForm, self).signup(request, user)

"""Forms for users."""

import logging

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, HTML
from django_select2.forms import Select2Widget
from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget

from django import forms

from .models import Profile
from .utils import create_userjobs_for

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
    """Customize django-allauth SignupForm to include tags."""

    tags = TagField(required=True, widget=LabelWidget)

    class Meta:
        """CustomSignupForm config info."""

        model = Profile
        fields = ('tags',)

    def __init__(self, *args, **kwargs):
        """Create a pretty crispy form."""
        logger.debug("Args: %s; kwargs: %s", args, kwargs)
        self.helper = FormHelper()
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
                HTML("""
                    <p><small>You must select at least one tag.  These tags
                     control which job postings will be shown to you and which
                     will not.  Only those jobs that match these tags will be
                     visible to you.  This can be changed later.</small></p>
                """),
                'tags'
            ),
            ButtonHolder(
                Submit('submit', 'Sign Up &raquo;')
            )
        )
        super(CustomSignupForm, self).__init__(*args, **kwargs)

    def signup(self, request, user):
        """Provide custom signup step (saving tags)."""
        tags = self.cleaned_data['tags']
        logger.info("User Signup: %s; request: %s; tags: %s", user, request, tags)
        user.profile.tags.add(*self.cleaned_data['tags'])
        user.profile.save()
        create_userjobs_for(user)

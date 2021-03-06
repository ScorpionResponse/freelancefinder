"""Forms for dealing with jobs/posts."""

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from taggit.models import Tag
from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget


class PostFilterForm(forms.Form):
    """Form for filtering the PostListView."""

    title = forms.CharField(required=False)
    is_freelance = forms.BooleanField(required=False)
    is_not_classified = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        """Create PostFilterForm with crispy form helpers."""
        super(PostFilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Filter'))


class JobSearchForm(forms.Form):
    """Form for filtering the JobListView."""

    search = forms.CharField(required=False)
    tag = forms.ModelChoiceField(queryset=Tag.objects.all().order_by('slug'), empty_label='All', to_field_name="slug", required=False)

    def __init__(self, *args, **kwargs):
        """Create JobSearchForm with crispy form helpers."""
        super(JobSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Search'))


class UserJobSearchForm(forms.Form):
    """Form for filtering the UserJobListView."""

    search = forms.CharField(required=False)
    # tag = forms.ModelChoiceField(queryset=Tag.objects.all().order_by('slug'), empty_label='All', to_field_name="slug", required=False)
    tag = TagField(required=False, widget=LabelWidget)

    def __init__(self, *args, **kwargs):
        """Create UserJobSearchForm with crispy form helpers."""
        super(UserJobSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Search'))

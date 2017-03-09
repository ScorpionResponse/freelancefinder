"""Forms for dealing with jobs/posts."""

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from taggit.models import Tag


class PostFilterForm(forms.Form):
    """Form for filtering the PostListView."""

    title = forms.CharField(required=False)
    is_job_posting = forms.BooleanField(required=False)
    is_freelance = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        """Create PostFilterForm with crispy form helpers."""
        super(PostFilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Filter'))


class JobSearchForm(forms.Form):
    """Form for filtering the JobListView."""

    TAG_CHOICES = [('', 'All')] + list(Tag.objects.all().values_list('slug', 'name').order_by('slug'))

    search = forms.CharField(required=False)
    tag = forms.ChoiceField(choices=TAG_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        """Create JobSearchForm with crispy form helpers."""
        super(JobSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Search'))

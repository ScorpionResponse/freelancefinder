"""Forms for dealing with jobs/posts."""

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class PostFilterForm(forms.Form):
    """Form for filtering the PostListView."""

    title = forms.CharField(required=False)
    is_job_posting = forms.BooleanField(required=False)
    is_freelance = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(PostFilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        # self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Filter'))

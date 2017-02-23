"""Forms for dealing with jobs/posts."""

from django import forms


class PostFilterForm(forms.Form):
    """Form for filtering the PostListView."""

    title = forms.CharField(required=False)
    is_job_posting = forms.BooleanField(required=False)
    is_freelance = forms.BooleanField(required=False)

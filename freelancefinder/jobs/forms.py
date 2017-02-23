"""Forms for dealing with jobs/posts."""

from django import forms


class PostFilterForm(forms.Form):
    """Form for filtering the PostListView."""

    title = forms.CharField()
    is_job_posting = forms.BooleanField()
    is_freelance = forms.BooleanField()

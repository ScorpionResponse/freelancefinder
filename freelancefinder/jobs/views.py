"""Pages relating to the jobs app."""
from django.views.generic import ListView

from .models import Job, Post


class JobListView(ListView):
    """List all jobs."""

    model = Job
    template_name = "jobs/job_list.html"


class PostListView(ListView):
    """List all Posts."""

    model = Post
    template_name = "jobs/post_list.html"

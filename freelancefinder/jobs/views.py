from django.views.generic import ListView

from .models import Job, Post


class JobListView(ListView):
    model = Job
    template_name = "jobs/job_list.html"


class PostListView(ListView):
    model = Post
    template_name = "jobs/post_list.html"

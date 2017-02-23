"""Pages relating to the jobs app."""
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from .forms import PostFilterForm
from .models import Job, Post


class JobListView(ListView):
    """List all jobs."""

    model = Job
    template_name = "jobs/job_list.html"


class PostListView(FormMixin, ListView):
    """List all Posts."""

    model = Post
    paginate_by = 20
    form_class = PostFilterForm
    template_name = "jobs/post_list.html"

    def get_queryset(self):
        return Post.objects.all().order_by('-created')

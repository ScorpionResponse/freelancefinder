"""Pages relating to the jobs app."""
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin

from .forms import PostFilterForm
from .models import Job, Post


class JobListView(ListView):
    """List all jobs."""

    model = Job
    paginate_by = 20
    template_name = "jobs/job_list.html"

    def get_queryset(self):
        """Queryset should sort by desc created by default."""
        return Job.objects.all().order_by('-created')


class JobDetailView(DetailView):
    """Show a single job."""

    model = Job


class PostListView(FormMixin, ListView):
    """List all Posts."""

    model = Post
    paginate_by = 20
    form_class = PostFilterForm
    template_name = "jobs/post_list.html"

    def get_queryset(self):
        """Queryset should sort by desc created by default."""
        return Post.objects.all().order_by('-created')

    def get_context_data(self, **kwargs):
        """Include search/filter form."""
        context = super(PostListView, self).get_context_data(**kwargs)

        context['form'] = self.get_form()

        return context

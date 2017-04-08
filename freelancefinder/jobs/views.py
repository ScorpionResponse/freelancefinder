"""Pages relating to the jobs app."""

import logging

from braces.views import GroupRequiredMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin

from .forms import PostFilterForm, JobSearchForm, FreelancerSearchForm
from .models import Job, Post, Freelancer

logger = logging.getLogger(__name__)


class FormGetMixin(FormMixin):
    """FormMixin which uses GET request data."""

    def get_form_kwargs(self):
        """Pull field values from GET data."""
        kwargs = {'initial': self.get_initial(), 'data': self.request.GET}
        return kwargs


class JobListView(LoginRequiredMixin, ListView, FormGetMixin):
    """List all jobs."""

    model = Job
    paginate_by = 20
    form_class = JobSearchForm
    template_name = "jobs/job_list.html"

    def get_queryset(self):
        """Queryset should sort by desc created by default."""
        search = self.request.GET.get('search', None)
        tags = self.request.GET.getlist('tag', None)
        querys = Job.objects.all().prefetch_related('posts', 'tags', 'posts__source')
        if search is not None and search != '':
            querys = querys.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if tags is not None and len(tags) > 0 and tags != ['']:
            querys = querys.filter(tags__slug__in=tags).distinct()
        logger.debug('Tags: %s', tags)
        logger.debug('Query: %s', str(querys.query))
        return querys.order_by('-created')

    def get_context_data(self, **kwargs):
        """Include search/filter form."""
        context = super(JobListView, self).get_context_data(**kwargs)

        context['form'] = self.get_form()

        return context


class JobDetailView(LoginRequiredMixin, DetailView):
    """Show a single job."""

    model = Job
    template_name = 'jobs/job_detail.html'


class FreelancerListView(LoginRequiredMixin, ListView, FormGetMixin):
    """List all freelancers."""

    model = Freelancer
    paginate_by = 20
    form_class = FreelancerSearchForm
    template_name = "jobs/freelancer_list.html"

    def get_queryset(self):
        """Queryset should sort by desc created by default."""
        search = self.request.GET.get('search', None)
        tag = self.request.GET.get('tag', None)
        querys = Freelancer.objects.all().prefetch_related('posts', 'tags', 'posts__source')
        if search is not None and search != '':
            querys = querys.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if tag is not None and tag != '':
            querys = querys.filter(tags__slug__in=[tag]).distinct()
        return querys.order_by('-created')

    def get_context_data(self, **kwargs):
        """Include search/filter form."""
        context = super(FreelancerListView, self).get_context_data(**kwargs)

        context['form'] = self.get_form()

        return context


class FreelancerDetailView(LoginRequiredMixin, DetailView):
    """Show a single freelancer."""

    model = Freelancer
    template_name = 'jobs/freelancer_detail.html'


class PostListView(GroupRequiredMixin, FormMixin, ListView):
    """List all Posts."""

    model = Post
    paginate_by = 20
    group_required = u'Administrators'
    form_class = PostFilterForm
    template_name = "jobs/post_list.html"

    def get_form_kwargs(self):
        """Use GET for form info."""
        kwargs = {'initial': self.get_initial(), 'data': self.request.GET}
        return kwargs

    def get_queryset(self):
        """Queryset should sort by desc created by default."""
        title = self.request.GET.get('title', None)
        is_job_posting = self.request.GET.get('is_job_posting', False)
        is_freelance = self.request.GET.get('is_freelance', False)
        is_freelancer = self.request.GET.get('is_freelancer', False)
        is_not_classified = self.request.GET.get('is_not_classified', False)
        querys = Post.objects.all().select_related('source')
        if is_not_classified:
            querys = querys.filter(is_job_posting=False, is_freelance=False, is_freelancer=False)
        else:
            if is_job_posting:
                querys = querys.filter(is_job_posting=True)
            if is_freelance:
                querys = querys.filter(is_freelance=True)
            if is_freelancer:
                querys = querys.filter(is_freelancer=True)
        if title is not None:
            querys = querys.filter(title__icontains=title)
        return querys.order_by('-created')

    def get_context_data(self, **kwargs):
        """Include search/filter form."""
        context = super(PostListView, self).get_context_data(**kwargs)

        context['form'] = self.get_form()

        return context

"""Pages relating to the jobs app."""

import logging

from braces.views import GroupRequiredMixin

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin

from .forms import PostFilterForm, JobSearchForm, UserJobSearchForm
from .models import Job, Post, UserJob

logger = logging.getLogger(__name__)


class FormGetMixin(FormMixin):
    """FormMixin which uses GET request data."""

    def get_form_kwargs(self):
        """Pull field values from GET data."""
        kwargs = {'initial': self.get_initial(), 'data': self.request.GET}
        return kwargs


class UserJobListView(LoginRequiredMixin, ListView, FormGetMixin):
    """List just this user's jobs."""

    model = UserJob
    paginate_by = 20
    form_class = UserJobSearchForm
    context_object_name = "userjob_list"
    template_name = "jobs/userjob_list.html"

    def get_queryset(self):
        """Perform filtering and sorting."""
        querys = UserJob.objects.filter(user=self.request.user)

        search = self.request.GET.get('search', None)
        tags = self.request.GET.getlist('tag', None)
        source = self.request.GET.get('source', None)
        if search is not None and search != '':
            querys = querys.filter(Q(job__title__icontains=search) | Q(job__description__icontains=search))
        if tags and tags != ['']:
            querys = querys.filter(job__tags__slug__in=tags).distinct()
        if source:
            querys = querys.filter(job__post__source__code=source)
        return querys.order_by('job__created').reverse()

    def get_source_facets(self):
        """Get Results faceted by Source."""
        querys = self.get_queryset()
        querys = querys.values('job__posts__source__name', 'job__posts__source__code').annotate(total=Count('job__posts__source')).order_by('job__posts__source__name')
        return querys

    def get_context_data(self, **kwargs):
        """Include search/filter form."""
        context = super(UserJobListView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['source_facets'] = self.get_source_facets()
        return context


class UserJobActionView(LoginRequiredMixin, View):
    """Accept button actions and return to post list."""

    def post(self, request):
        """Take the action then redirect to list."""
        userjob_id = request.POST.get('userjob_id', None)
        redirect_to = request.POST.get('next', reverse('userjob-list'))
        action = 'break'
        if 'dismiss' in request.POST:
            action = 'dismiss'

        if userjob_id is None or action == 'break':
            raise Exception('No action specified.')

        logger.info('UserJob ID %s taking action %s', userjob_id, action)
        action_userjob = get_object_or_404(UserJob, pk=userjob_id)
        if action == 'dismiss':
            action_userjob.delete()
            messages.success(request, "Opportunity {} dismissed.".format(action_userjob))

        action_userjob.save()
        return HttpResponseRedirect(redirect_to)


class JobListView(LoginRequiredMixin, ListView, FormGetMixin):
    """List all jobs."""

    model = Job
    paginate_by = 20
    form_class = JobSearchForm
    context_object_name = 'job_list'
    template_name = "jobs/job_list.html"

    def get_queryset(self):
        """Queryset should sort by desc created by default."""
        search = self.request.GET.get('search', None)
        tags = self.request.GET.getlist('tag', None)
        querys = Job.objects.all().prefetch_related('posts', 'tags', 'posts__source')
        if search is not None and search != '':
            querys = querys.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if tags and tags != ['']:
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


class PostListView(GroupRequiredMixin, FormMixin, ListView):
    """List all Posts."""

    model = Post
    context_object_name = 'post_list'
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
        is_freelance = self.request.GET.get('is_freelance', False)
        is_not_classified = self.request.GET.get('is_not_classified', False)
        querys = Post.objects.all().select_related('source')
        if is_not_classified:
            querys = querys.filter(is_freelance=False)
        else:
            if is_freelance:
                querys = querys.filter(is_freelance=True)
        if title is not None:
            querys = querys.filter(title__icontains=title)
        return querys.order_by('-created')

    def get_context_data(self, **kwargs):
        """Include search/filter form."""
        context = super(PostListView, self).get_context_data(**kwargs)

        context['form'] = self.get_form()

        return context


class PostActionView(GroupRequiredMixin, View):
    """Accept button actions and return to post list."""

    group_required = u'Administrators'

    def post(self, request):
        """Take the action then redirect to list."""
        post_id = request.POST.get('post_id', None)
        redirect_to = request.POST.get('next', reverse('post-list'))
        action = 'break'
        if 'accept' in request.POST:
            action = 'accept'
        elif 'dismiss' in request.POST:
            action = 'dismiss'

        if post_id is None or action == 'break':
            raise Exception('No action specified.')

        logger.info('Post ID %s taking action %s', post_id, action)
        action_post = get_object_or_404(Post, pk=post_id)
        if action == 'dismiss':
            action_post.garbage = True
        elif action == 'accept':
            action_post.is_freelance = True

        action_post.save()
        return HttpResponseRedirect(redirect_to)

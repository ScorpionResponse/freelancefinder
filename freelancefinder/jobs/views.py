"""Pages relating to the jobs app."""

import datetime
import logging

from braces.views import GroupRequiredMixin

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.db.models.functions import TruncDate
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin

from users.utils import my_next_run

from .forms import PostFilterForm, JobSearchForm, UserJobSearchForm
from .models import Job, Post, UserJob

logger = logging.getLogger(__name__)


class FormGetMixin(FormMixin):
    """FormMixin which uses GET request data."""

    def get_form_kwargs(self):
        """Pull field values from GET data."""
        kwargs = {'initial': self.get_initial(), 'data': self.request.GET}
        return kwargs


class UserJobRedirectView(LoginRequiredMixin, RedirectView):
    """Get date and redirect."""

    permanent = False
    pattern_name = 'userjob-list'
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        """Insert a default date and redirect."""
        now = timezone.now()
        redirect_date = now - datetime.timedelta(days=1)

        first_userjob = UserJob.objects.filter(user=self.request.user).order_by('job__created').reverse().first()
        if first_userjob:
            redirect_date = first_userjob.job.created
        kwargs['date'] = redirect_date.strftime("%Y-%m-%d")
        return super(UserJobRedirectView, self).get_redirect_url(*args, **kwargs)


class UserJobListView(LoginRequiredMixin, ListView, FormGetMixin):
    """List just this user's jobs."""

    model = UserJob
    form_class = UserJobSearchForm
    context_object_name = "userjob_list"
    template_name = "jobs/userjob_list.html"

    def __base_queryset(self):
        """Build the base queryset for the view."""
        # today = timezone.now().date()
        # return UserJob.objects.filter(user=self.request.user).exclude(job__created__date=today)
        return UserJob.objects.filter(user=self.request.user)

    def __form_filtered_queryset(self):
        """Filter by the form fields."""
        querys = self.__base_queryset()

        search = self.request.GET.get('search', None)
        tags = self.request.GET.getlist('tag', None)
        if search is not None and search != '':
            querys = querys.filter(Q(job__title__icontains=search) | Q(job__description__icontains=search))
        if tags and tags != ['']:
            querys = querys.filter(job__tags__slug__in=tags).distinct()
        return querys

    def get_queryset(self):
        """Perform filtering and sorting."""
        date = self.kwargs['date']
        querys = self.__form_filtered_queryset()
        querys = querys.filter(job__created__date=date)
        source = self.request.GET.get('source', None)
        if source:
            querys = querys.filter(job__posts__source__code=source)
        return querys.order_by('job__created').reverse()

    def get_source_facets(self):
        """Get Results faceted by Source."""
        querys = self.__form_filtered_queryset()
        querys = querys.values('job__posts__source__name', 'job__posts__source__code').annotate(total=Count('job__posts__source')).order_by('job__posts__source__name')
        return querys

    def get_date_facets(self):
        """Get results faceted by created."""
        querys = self.__form_filtered_queryset()
        source = self.request.GET.get('source', None)
        if source:
            querys = querys.filter(job__posts__source__code=source)
        querys = querys.values(created_date=TruncDate('job__created')).annotate(total=Count(TruncDate('job__created'))).order_by('created_date').reverse()
        return querys

    def get_context_data(self, **kwargs):
        """Include search/filter form."""
        context = super(UserJobListView, self).get_context_data(**kwargs)
        context['curdate'] = self.kwargs['date']
        context['form'] = self.get_form()
        context['source_facets'] = self.get_source_facets()
        context['date_facets'] = self.get_date_facets()
        context['my_next_run'] = my_next_run(self.request.user)
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
        source = self.request.GET.get('source', None)
        is_freelance = self.request.GET.get('is_freelance', False)
        is_not_classified = self.request.GET.get('is_not_classified', True)
        querys = Post.objects.filter(processed=True).select_related('source')
        if is_not_classified:
            querys = querys.filter(is_freelance=False)
        else:
            if is_freelance:
                querys = querys.filter(is_freelance=True)
        if title is not None:
            querys = querys.filter(title__icontains=title)
        if source:
            querys = querys.filter(source__code=source)
        return querys.order_by('-created')

    def get_source_facets(self):
        """Get Results faceted by Source."""
        querys = self.get_queryset()
        querys = querys.values('source__name', 'source__code').annotate(total=Count('source')).order_by('source__name')
        return querys

    def get_context_data(self, **kwargs):
        """Include search/filter form."""
        context = super(PostListView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['source_facets'] = self.get_source_facets()
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

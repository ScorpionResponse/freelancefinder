from django.views.generic.base import TemplateView


class AllJobsView(TemplateView):

    template_name = "jobs/all_jobs.html"

"""Simple models to track information related to a particular job/posting."""

from future.utils import python_2_unicode_compatible
from model_utils.models import TimeStampedModel

from django.db import models


class PostManager(models.Manager):
    """Manager for Posts."""

    def new(self):
        """Get unprocessed Posts."""
        return self.get_queryset().filter(processed=False).order_by('created')

    def pending_freelance_jobs(self):
        """Get only freelance job posts which are not linked."""
        return self.get_queryset().filter(is_freelance=True, is_job_posting=True, job__isnull=True).order_by('created')


@python_2_unicode_compatible
class Post(TimeStampedModel):
    """
    Simple model for tracking a Post.

    A Post is a particular page on the internet where an announcement for a
    postition was found.
    """

    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name="posts", blank=True, null=True)
    url = models.URLField()
    source = models.ForeignKey('remotes.Source', on_delete=models.SET_NULL, blank=True, null=True, related_name="posts")
    subarea = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    unique = models.CharField(max_length=255)
    is_job_posting = models.BooleanField(default=False)
    is_freelance = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    objects = PostManager()

    class Meta:
        """Meta info for Post."""

        unique_together = ("source", "unique")

    def __str__(self):
        """Representation for a Post."""
        return u"<Post ID:{}; Unique:{}; Title:{}>".format(self.pk, self.unique, self.title)


@python_2_unicode_compatible
class Job(TimeStampedModel):
    """A Job is the actual opportunity.  There may be many Posts about the same Job."""

    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        """Representation for a Job."""
        return u"<Job ID:{}; Title:{}>".format(self.pk, self.title)

"""Simple models to track information related to a particular job/posting."""

import datetime

from future.utils import python_2_unicode_compatible

from django.db import models


@python_2_unicode_compatible
class Post(models.Model):
    """
    Simple model for tracking a Post.

    A Post is a particular page on the internet where an announcement for a
    postition was found.
    """

    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name="posts", blank=True, null=True)
    url = models.URLField()
    source = models.ForeignKey('remotes.Source', on_delete=models.SET_NULL, blank=True, null=True, related_name="posts")
    date_added = models.DateTimeField(default=datetime.datetime.now)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        """Representation for a Post."""
        return u"<Post ID:{}; Title:{}>".format(self.pk, self.title)


@python_2_unicode_compatible
class Job(models.Model):
    """A Job is the actual opportunity.  There may be many Posts about the same Job."""

    date_added = models.DateTimeField(default=datetime.datetime.now)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        """Representation for a Job."""
        return u"<Job ID:{}; Title:{}>".format(self.pk, self.title)


import datetime

from django.db import models


class Post(models.Model):

    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name="posts")
    url = models.URLField()
    source = models.ForeignKey('remotes.Source', on_delete=models.SET_NULL, blank=True, null=True, related_name="posts")
    date_added = models.DateTimeField(default=datetime.datetime.now)
    title = models.CharField(max_length=255)
    description = models.TextField()


class Job(models.Model):

    date_added = models.DateTimeField(default=datetime.datetime.now)
    title = models.CharField(max_length=255)
    description = models.TextField()

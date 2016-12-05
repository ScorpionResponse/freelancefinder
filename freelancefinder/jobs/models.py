
import datetime

from django.db import models


class Post(models.Model):

    url = models.URLField()
    source = models.ForeignKey('remotes.Source', on_delete=models.SET_NULL, blank=True, null=True, related_name="posts")
    date_added = models.DateTimeField(default=datetime.datetime.now)
    description = models.TextField()

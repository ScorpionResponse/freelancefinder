from django.db import models


class Source(models.Model):

    name = models.CharField(max_length=20, primary_key=True)
    url = models.URLField()

"""Models for remotes app."""
from django.db import models


class Source(models.Model):
    """Website where jobs may be posted."""

    name = models.CharField(max_length=20, primary_key=True)
    url = models.URLField()

    def __str__(self):
        """Representation for a Source."""
        return "<Source ID:{}; Name:{}>".format(self.pk, self.name)

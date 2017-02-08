"""Models for remotes app."""

from future.utils import python_2_unicode_compatible

from django.db import models


@python_2_unicode_compatible
class Source(models.Model):
    """Website where jobs may be posted."""

    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200)
    url = models.URLField()

    def __str__(self):
        """Representation for a Source."""
        return u"<Source Code:{}; Name:{}>".format(self.code, self.name)

    def harvester(self):
        """Get the harvester for this source."""
        source_harvester = None
        if self.code == "reddit":
            from .sources.reddit.harvest import Harvester

        source_harvester = Harvester(self)
        return source_harvester

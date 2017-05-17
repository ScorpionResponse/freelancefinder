"""Models for remotes app."""

from future.utils import python_2_unicode_compatible

from model_utils import Choices

from django.db import models


@python_2_unicode_compatible
class Source(models.Model):
    """Website where jobs may be posted."""

    HARVEST_TYPE = Choices('rss_feed', 'custom')

    code = models.CharField(max_length=40, primary_key=True)
    name = models.CharField(max_length=200)
    url = models.URLField()
    harvest_type = models.CharField(choices=HARVEST_TYPE, default=HARVEST_TYPE.custom, max_length=20)

    def __str__(self):
        """Representation for a Source."""
        return u"<Source Code:{}; Name:{}>".format(self.code, self.name)

    def harvester(self):
        """Get the harvester for this source."""
        source_harvester = None
        if self.harvest_type == self.HARVEST_TYPE.custom:
            if self.code == "reddit":
                from .sources.reddit.harvest import Harvester
            elif self.code == 'hackernews':
                from .sources.hackernews.harvest import Harvester
            elif self.code == 'fossjobs':
                from .sources.fossjobs.harvest import Harvester
            elif self.code == 'trabajospython':
                from .sources.trabajospython.harvest import Harvester
            elif self.code == 'workinstartups':
                from .sources.workinstartups.harvest import Harvester
            elif self.code == 'workingnomads':
                from .sources.workingnomads.harvest import Harvester

        elif self.harvest_type == self.HARVEST_TYPE.rss_feed:
            from .sources.rss_feed.harvest import Harvester

        source_harvester = Harvester(self)
        return source_harvester


@python_2_unicode_compatible
class SourceConfig(models.Model):
    """Config values for Sources."""

    source = models.ForeignKey("Source", on_delete=models.CASCADE, related_name="config")
    config_key = models.CharField(max_length=100)
    config_value = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        """Config value."""
        return u"<SourceConfig:{}; K:{}; V:{}".format(self.pk, self.config_key, self.config_value)

    class Meta:
        """Meta info for SourceConfig."""

        unique_together = ("source", "config_key")

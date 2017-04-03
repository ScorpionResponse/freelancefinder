"""Models for remotes app."""

import datetime

from future.utils import python_2_unicode_compatible
import wrapt

from django.db import models


def periodically(source, period='daily', check_name='last_processed'):
    """Ensure that the wrapped function only runs once per period."""

    timecheck = None

    if period == 'daily':
        timecheck = datetime.datetime.today().strftime("%Y-%m-%d")
    elif period == 'hourly':
        timecheck = datetime.datetime.today().strftime("%Y-%m-%d-%H")

    if source.config.filter(config_key=check_name, config_value=timecheck).exists():
        return None
    source.config.update_or_create(config_key=check_name, defaults={'config_value': timecheck})

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        """Wrap function to enfore period."""
        return wrapped(*args, **kwargs)
    return wrapper


@python_2_unicode_compatible
class Source(models.Model):
    """Website where jobs may be posted."""

    code = models.CharField(max_length=40, primary_key=True)
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
        elif self.code == 'hackernews':
            from .sources.hackernews.harvest import Harvester
        elif self.code == 'fossjobs':
            from .sources.fossjobs.harvest import Harvester

        source_harvester = Harvester()
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

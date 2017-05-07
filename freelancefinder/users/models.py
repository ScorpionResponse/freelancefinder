"""Models related to users."""

import logging
from future.utils import python_2_unicode_compatible

from model_utils import Choices
from taggit.managers import TaggableManager
from timezone_utils.fields import TimeZoneField
from timezone_utils.choices import PRETTY_ALL_TIMEZONES_CHOICES as TIMEZONE_CHOICES

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Profile(models.Model):
    """Hold user profile options not in default user model."""

    REFRESH_FREQUENCY = Choices(('daily', _('Daily')), ('twice_a_day', _('Twice a Day')), ('hourly', _('Hourly')))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    custom_timezone = TimeZoneField(choices=TIMEZONE_CHOICES, default='America/New_York')
    refresh_frequency = models.CharField(choices=REFRESH_FREQUENCY, default=REFRESH_FREQUENCY.daily, max_length=20)
    tags = TaggableManager(blank=True)

    def __str__(self):
        """Representation of a profile."""
        return u"<Profile ID:{}; User ID:{}; Timezone:{}>".format(self.pk, self.user_id, self.custom_timezone)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """If a new user is created, also create a profile."""
    logger.debug('Create Or Update User Profile caught signal from sender: %s, instance: %s, created: %s, kwargs: %s', sender, instance, created, kwargs)
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

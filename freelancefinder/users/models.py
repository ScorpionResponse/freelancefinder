"""Models related to users."""

import logging
from future.utils import python_2_unicode_compatible

from timezone_utils.choices import PRETTY_ALL_TIMEZONES_CHOICES as TIMEZONE_CHOICES

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Profile(models.Model):
    """Hold user profile options not in default user model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    custom_timezone = models.CharField(choices=TIMEZONE_CHOICES, max_length=100, default='America/New_York')

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

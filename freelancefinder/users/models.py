"""Models related to users."""

import logging
from future.utils import python_2_unicode_compatible

from model_utils import Choices
from taggit.managers import TaggableManager
from timezone_utils.fields import TimeZoneField
from timezone_utils.choices import PRETTY_ALL_TIMEZONES_CHOICES as TIMEZONE_CHOICES

from django.contrib.auth.models import User, Group
from django.core.mail import mail_managers
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Profile(models.Model):
    """Hold user profile options not in default user model."""

    REFRESH_FREQUENCY = Choices(('daily', _('Daily')), ('twice_a_day', _('Twice a Day')), ('hourly', _('Hourly')))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", unique=True)
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


@python_2_unicode_compatible
class Account(models.Model):
    """Track internal accounting/other info about this user."""

    SUBSCRIPTION_MODELS = Choices('yearly', 'monthly')

    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name="account", blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_subscription_created = models.DateTimeField(blank=True, null=True)
    subscription = models.CharField(choices=SUBSCRIPTION_MODELS, max_length=100, blank=True, null=True)

    def __str__(self):
        """Representation of a user account."""
        return u"<Account ID:{}; User ID: {}>".format(self.pk, self.user_id)

    def confirm_payment(self):
        """Confirm the payment of this account."""
        group = Group.objects.get(name='Paid')
        self.user.groups.add(group)
        self.user.save()


@receiver(post_save, sender=User)
def create_or_update_user_account(sender, instance, created, **kwargs):
    """If a new user is created, also create an account."""
    logger.debug('Create Or Update User Account caught signal from sender: %s, instance: %s, created: %s, kwargs: %s', sender, instance, created, kwargs)
    if created:
        Account.objects.create(user=instance)
    instance.account.save()


@receiver(post_save, sender=User)
def first_time_user_flow(sender, instance, created, **kwargs):
    """If a new user is created, also create an account."""
    logger.debug('First Time User Flow caught signal from sender: %s, instance: %s, created: %s, kwargs: %s', sender, instance, created, kwargs)
    if created:
        logger.info("New User Created: %s", instance)
        mail_managers(subject="New User: %s" % (instance,), message="New User:\n\t%s\n\t%s\n" % (instance, instance.email), fail_silently=True)

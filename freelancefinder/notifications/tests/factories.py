"""Notification factories."""

import factory
import factory.fuzzy
from django_factory_boy.auth import UserFactory

# pylint: disable=too-few-public-methods


class MessageFactory(factory.django.DjangoModelFactory):
    """Message factory."""

    url = factory.LazyAttribute(lambda x: '%s/' % factory.Faker('uri_path', deep=2))
    factory.Faker('uri_path', deep=2)
    subject = factory.Faker('name')
    email_body = factory.Faker('paragraphs', nb=3)
    slack_body = factory.Faker('paragraphs', nb=1)

    class Meta(object):
        """Config for MessageFactory."""

        model = 'notifications.Message'


class NotificationFactory(factory.django.DjangoModelFactory):
    """Notification factory."""

    notification_type = factory.fuzzy.FuzzyChoice(['signup', 'welcome_package', 'one_time', 'expiration'])
    message = factory.SubFactory(MessageFactory)
    user = factory.SubFactory(UserFactory)

    class Meta(object):
        """Config for NotificationFactory."""

        model = 'notifications.Notification'


class NotificationHistoryFactory(factory.django.DjangoModelFactory):
    """NotificationHistory factory."""

    user = factory.SubFactory(UserFactory)
    notification = factory.SubFactory(NotificationFactory)
    sent = factory.Faker('pybool')
    sent_at = factory.Faker('datetime')

    class Meta(object):
        """Config for NotificationHistoryFactory."""

        model = 'notifications.NotificationHistory'

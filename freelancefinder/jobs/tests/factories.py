"""Object factories."""

import factory
from faker import Factory as FakerFactory

FAKER = FakerFactory.create()

# pylint: disable=too-few-public-methods


class JobFactory(factory.django.DjangoModelFactory):
    """Job factory."""

    title = factory.LazyAttribute(lambda x: FAKER.job())
    description = factory.LazyAttribute(lambda x: FAKER.text(max_nb_chars=500))

    class Meta(object):
        """Config for JobFactory."""

        model = 'jobs.Job'


class FreelancerFactory(factory.django.DjangoModelFactory):
    """Freelancer factory."""

    title = factory.LazyAttribute(lambda x: FAKER.name())
    description = factory.LazyAttribute(lambda x: FAKER.text(max_nb_chars=500))

    class Meta(object):
        """Config for FreelancerFactory."""

        model = 'jobs.Freelancer'


class SourceFactory(factory.django.DjangoModelFactory):
    """Source Factory."""

    code = factory.Sequence(lambda n: 'code-%d' % n)
    name = factory.LazyAttribute(lambda x: FAKER.name())
    url = factory.LazyAttribute(lambda x: FAKER.url())

    class Meta(object):
        """Config for SourceFactory."""

        model = 'remotes.Source'


class PostFactory(factory.django.DjangoModelFactory):
    """Post factory."""

    url = factory.LazyAttribute(lambda x: FAKER.url())
    title = factory.LazyAttribute(lambda x: FAKER.job())
    description = factory.LazyAttribute(lambda x: FAKER.text(max_nb_chars=500))
    unique = factory.Sequence(lambda n: 'unique-%d' % n)
    source = factory.SubFactory(SourceFactory)
    subarea = factory.Sequence(lambda n: 'subarea-%d' % n)
    job = factory.SubFactory(JobFactory)

    class Meta(object):
        """Config for PostFactory."""

        model = 'jobs.Post'

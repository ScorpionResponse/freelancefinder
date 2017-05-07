"""Object factories."""

import factory
from faker import Factory as FakerFactory
from django_factory_boy.auth import UserFactory

FAKER = FakerFactory.create()

# pylint: disable=too-few-public-methods


class TagFactory(factory.django.DjangoModelFactory):
    """Tag factory."""

    name = factory.LazyAttribute(lambda x: FAKER.name() + FAKER.uuid4())

    class Meta(object):
        """Config for TagFactory."""

        model = 'taggit.Tag'


class JobFactory(factory.django.DjangoModelFactory):
    """Job factory."""

    title = factory.LazyAttribute(lambda x: FAKER.job())
    description = factory.LazyAttribute(lambda x: FAKER.text(max_nb_chars=500))

    class Meta(object):
        """Config for JobFactory."""

        model = 'jobs.Job'

    @factory.post_generation
    def create_tags(self, create, extracted):
        """Generate tags."""
        if not create:
            return
        tags = ['job', 'django', 'soup']
        if extracted:
            tags = extracted
        for tag in tags:
            self.tags.add(tag)


class UserJobFactory(factory.django.DjangoModelFactory):
    """UserJob Factory."""

    job = factory.SubFactory(JobFactory)
    user = factory.SubFactory(UserFactory)

    class Meta(object):
        """Config for userjobfactory."""

        model = 'jobs.UserJob'


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
    is_freelance = factory.LazyAttribute(lambda x: FAKER.pybool())
    processed = factory.LazyAttribute(lambda x: FAKER.pybool())
    job = factory.SubFactory(JobFactory)

    class Meta(object):
        """Config for PostFactory."""

        model = 'jobs.Post'

    @factory.post_generation
    def create_tags(self, create, extracted):
        """Generate tags."""
        if not create:
            return
        tags = ['job', 'django', 'soup']
        if extracted:
            tags = extracted
        for tag in tags:
            self.tags.add(tag)

"""Simple models to track information related to a particular job/posting."""

from future.utils import python_2_unicode_compatible
from model_utils.models import TimeStampedModel
from nltk import bigrams
from taggit.managers import TaggableManager
from taggit.models import Tag

from django.db import models

from utils.text import generate_fingerprint


class PostManager(models.Manager):
    """Manager for Posts."""

    def get_queryset(self):
        """Remove garbage."""
        return super(PostManager, self).get_queryset().filter(garbage=False)

    def new(self):
        """Get unprocessed Posts."""
        return self.get_queryset().filter(processed=False).order_by('created')

    def pending_freelance_jobs(self):
        """Get only freelance job posts which are not linked."""
        return self.get_queryset().filter(is_freelance=True, job__isnull=True).order_by('created')


@python_2_unicode_compatible
class Post(TimeStampedModel):
    """
    Simple model for tracking a Post.

    A Post is a particular page on the internet where an announcement for a
    postition was found.
    """

    job = models.ForeignKey('Job', on_delete=models.SET_NULL, related_name="posts", blank=True, null=True)
    url = models.URLField()
    source = models.ForeignKey('remotes.Source', on_delete=models.SET_NULL, blank=True, null=True, related_name="posts")
    subarea = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    unique = models.CharField(max_length=255)
    is_freelance = models.BooleanField(default=False)
    garbage = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    objects = PostManager()
    tags = TaggableManager()

    class Meta:
        """Meta info for Post."""

        unique_together = ("source", "unique")

    def __str__(self):
        """Representation for a Post."""
        return u"<Post ID:{}; Unique:{}; Title:{}>".format(self.pk, self.unique, self.title)

    def exists(self):
        """Determine if the post already exists in the database."""
        return self.pk is not None or Post.objects.filter(source=self.source, unique=self.unique).exists()

    @property
    def taggable_words(self):
        """Get all taggable words for this post."""
        title_words = self.title.replace(',', '').replace('/', ' ').split(' ')
        description_words = self.description.replace(', ', '').replace('/', ' ').split(' ')
        joined_words = [' '.join(x) for x in list(bigrams(description_words))]
        areas = [self.subarea]

        tag_words = title_words + description_words + joined_words + areas
        tag_words = [x.lower() for x in tag_words if x is not None]
        return tag_words


@python_2_unicode_compatible
class Job(TimeStampedModel):
    """A Job is the actual opportunity.  There may be many Posts about the same Job."""

    title = models.CharField(max_length=255)
    description = models.TextField()
    fingerprint = models.CharField(max_length=255)
    tags = TaggableManager()

    def __str__(self):
        """Representation for a Job."""
        return u"<Job ID:{}; Title:{}>".format(self.pk, self.title)

    def save(self, *args, **kwargs):
        """Add fingerprint and save."""
        if not self.pk:
            self.fingerprint = generate_fingerprint(self.title + ' ' + self.description)
        super(Job, self).save(*args, **kwargs)

    @property
    def taggable_words(self):
        """Get all taggable words for this job."""
        title_words = self.title.replace(',', '').replace('/', ' ').split(' ')
        description_words = self.description.replace(', ', '').replace('/', ' ').split(' ')
        joined_words = [' '.join(x) for x in list(bigrams(description_words))]
        areas = list(self.posts.all().values_list('subarea', flat=True))

        tag_words = title_words + description_words + joined_words + areas
        tag_words = [x.lower() for x in tag_words if x is not None]
        return tag_words


class TagVariantManager(models.Manager):
    """Manager for TagVariants."""

    def get_queryset(self):
        """Remove job."""
        return super(TagVariantManager, self).get_queryset().filter(variant='job')

    def all_tags(self):
        """Return a dict of lower case tag: Tag Name."""
        all_tags = list(Tag.objects.all().values_list('name', flat=True))
        all_tags = {x.lower(): x for x in all_tags}
        variant_tags = {variant: tag for variant, tag in self.get_queryset().values_list('variant', 'tag__name')}
        all_tags.update(variant_tags)
        return all_tags


@python_2_unicode_compatible
class TagVariant(models.Model):
    """A TagVariant will map several versions of a tag to one normalized Tag."""

    variant = models.CharField(max_length=255)
    tag = models.ForeignKey("taggit.Tag", on_delete=models.CASCADE)
    objects = TagVariantManager()

    def __str__(self):
        """Representation of a TagVariant."""
        return u"<TagVariant ID:{}; Variant:{}; Tag:{}>".format(self.pk, self.variant, self.tag.name)

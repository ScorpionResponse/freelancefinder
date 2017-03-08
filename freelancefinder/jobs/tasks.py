"""Tasks to handle periodic tasks for jobs."""

from celery import Celery
from celery.utils.log import get_task_logger


celery_app = Celery()
logger = get_task_logger(__name__)


@celery_app.task
def process_new_posts():
    """Determine which posts are about freelance jobs."""
    from .models import Post

    for post in Post.objects.new():
        logger.debug("Processing post: %s", post)
        post.processed = True
        if '[hiring]' in post.title.lower():
            post.is_job_posting = True
            post.is_freelance = True
        post.save()


@celery_app.task
def create_jobs():
    """Create a Job from a Post."""
    from .models import Post, Job

    for post in Post.objects.pending_freelance_jobs():
        logger.debug("Creating job from post: %s", post)
        job = Job.objects.create(title=post.title, description=post.description)
        post.job = job
        post.save()


@celery_app.task
def tag_jobs():
    """Add tags for jobs."""
    from nltk import bigrams
    from taggit.models import Tag
    from .models import Job

    all_tags = list(Tag.objects.all().values_list('name', flat=True))
    all_tags = [x.lower() for x in all_tags]
    logger.info('Got all tags list: %s', all_tags)

    for job in Job.objects.filter(tags__isnull=True):
        title_words = job.title.split(' ')
        description_words = job.description.split(' ')
        joined_words = [' '.join(x) for x in list(bigrams(description_words))]
        areas = list(job.posts.all().values_list('subarea', flat=True))

        taggable_words = title_words + description_words + joined_words + areas
        taggable_words = [x.lower() for x in taggable_words if x is not None]
        logger.info('Job: %s - All Taggable Words: %s', job, taggable_words)
        for word in set(taggable_words):
            if word in all_tags:
                logger.info('Add tag %s to job %s', word, job)
                job.tags.add(word)
        job.tags.add('job')
        job.save()

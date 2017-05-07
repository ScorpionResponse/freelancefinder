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
        current_tags = post.tags.names()
        if 'Full Time' in current_tags:
            logger.info('Marking Full Time job post as garbage: %s', post)
            post.garbage = True
        if 'For Hire' in current_tags:
            logger.info('Marking For Hire job post as garbage: %s', post)
            post.garbage = True

        freelance_tags = ['Hiring', 'Part Time', 'Freelance']
        if any(tag in current_tags for tag in freelance_tags):
            post.is_freelance = True
        post.save()


@celery_app.task
def create_jobs():
    """Create a Job from a Post."""
    from .models import Post, Job
    from utils.text import generate_fingerprint

    for post in Post.objects.pending_freelance_jobs():
        logger.debug("Creating job from post: %s", post)
        fingerprint = generate_fingerprint(post.title + " " + post.description)
        potential_matches = Job.objects.filter(fingerprint=fingerprint)
        if len(potential_matches) == 1:
            post.job = potential_matches.first()
            logger.info('Found Existing job to match post to: %s', post.job)
            post.save()
        else:
            job = Job.objects.create(title=post.title, description=post.description, created=post.created)
            post.job = job
            post.save()


@celery_app.task
def create_userjobs():
    """Link Users and Jobs."""
    from django.contrib.auth.models import User
    from users.utils import create_userjobs_for

    logger.info("Creating user jobs.")
    for user in User.objects.all():
        create_userjobs_for(user)


@celery_app.task
def tag_posts():
    """Add tags for posts."""
    from .models import Post, TagVariant

    all_tags = TagVariant.objects.all_tags()

    for post in Post.objects.filter(tags__isnull=True):
        taggable_words = post.taggable_words
        logger.info('Post: %s - All Taggable Words: %s', post, taggable_words)
        for word in set(taggable_words):
            if word in all_tags:
                logger.info('Add tag %s to post %s', all_tags[word], post)
                post.tags.add(all_tags[word])
        post.tags.add('post')
        post.save()


@celery_app.task
def tag_jobs():
    """Add tags for jobs."""
    from .models import Job, TagVariant

    all_tags = TagVariant.objects.all_tags()

    for job in Job.objects.filter(tags__isnull=True):
        taggable_words = job.taggable_words
        logger.info('Job: %s - All Taggable Words: %s', job, taggable_words)
        for word in set(taggable_words):
            if word in all_tags:
                logger.info('Add tag %s to job %s', all_tags[word], job)
                job.tags.add(all_tags[word])
        job.tags.add('job')
        job.save()

"""Tasks to handle periodic tasks for jobs."""

from celery import Celery
from celery.utils.log import get_task_logger


celery_app = Celery()
logger = get_task_logger(__name__)

FAIL_TAGS = ['Full Time', 'Equity', 'For Hire', 'Permanent', 'Dental']
PASS_TAGS = ['Hiring', 'Contract', 'Part Time', 'Freelance']


@celery_app.task
def process_new_posts():
    """Determine which posts are about freelance jobs."""
    from datetime import datetime, timedelta
    from .models import Post

    today = datetime.today()
    a_month_ago = today - timedelta(days=31)

    for post in Post.objects.new():
        logger.info("Processing post: %s", post)
        post.processed = True
        current_tags = post.tags.names()
        if any(tag in current_tags for tag in FAIL_TAGS):
            logger.info('Marking post as garbage for tags: %s', post)
            post.garbage = True
        elif post.created < a_month_ago:
            logger.info('Marking post as garbage due to age: %s', post)
            post.garbage = True
        elif any(tag in current_tags for tag in PASS_TAGS):
            logger.info('Marking post as freelance for tags: %s', post)
            post.is_freelance = True
        post.save()


@celery_app.task
def create_jobs():
    """Create a Job from a Post."""
    from .models import Post, Job
    from utils.text import generate_fingerprint

    for post in Post.objects.pending_freelance_jobs():
        logger.info("Creating job from post: %s", post)
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
def create_userjobs(frequency):
    """Link Users and Jobs."""
    from users.utils import create_userjobs_for, users_with_frequency

    logger.info("Starting User Job Creation for interval: %s", frequency)
    for user in users_with_frequency(frequency):
        logger.info("Creating user jobs (%s) for user: %s.", frequency, user)
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

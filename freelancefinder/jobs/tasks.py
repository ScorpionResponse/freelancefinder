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

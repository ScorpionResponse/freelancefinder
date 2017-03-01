"""Tasks to handle periodic tasks for jobs."""

from django_celery_beat.models import IntervalSchedule, PeriodicTask
from celery import Celery
from celery.utils.log import get_task_logger


celery_app = Celery()
logger = get_task_logger(__name__)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Ensure periodic tasks are scheduled."""
    logger.info("Configuring periodic tasks.")
    logger.debug('Sender: %s; kwargs: %s', sender, kwargs)

    schedule, created = IntervalSchedule.objects.get_or_create(every=4, period=IntervalSchedule.MINUTES)
    logger.debug("IntervalSchedule: %s; Created: %s", schedule, created)

    pertask, created = PeriodicTask.objects.get_or_create(interval=schedule, name="Process New Posts", task='jobs.tasks.process_new_posts')
    logger.debug("PeriodicTask: %s; Created: %s", pertask, created)
    pertask, created = PeriodicTask.objects.get_or_create(interval=schedule, name="Create Jobs from Posts", task='jobs.tasks.create_jobs')
    logger.debug("PeriodicTask: %s; Created: %s", pertask, created)


@celery_app.task
def process_new_posts():
    """Determine which posts are about freelance jobs."""
    from .models import Post

    for post in Post.objects.new():
        post.processed = True
        if '[hiring]' in post.title.lower():
            post.is_job_posting = True
            post.is_freelance = True
        post.save()


@celery_app.task
def create_jobs():
    """Create a Job from a Post."""
    from .models import Post

    for post in Post.objects.pending_freelance_jobs():
        post.job.create(title=post.title, description=post.description)

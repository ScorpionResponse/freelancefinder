"""Tasks to perform periodic tasks with remotes."""

from celery.utils.log import get_task_logger

from freelancefinder import celery_app

logger = get_task_logger(__name__)


@celery_app.task
def harvest_sources():
    """Get a new batch of data from all sources."""
    from .models import Source
    for source in Source.objects.all():
        logger.info("Harvesting from Source: %s", source)
        harvester = source.harvester()
        for post in harvester.harvest():
            logger.info("Got new Post: %s", post)

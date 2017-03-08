"""Harvest process for the HackerNews Source."""

from collections import defaultdict
import logging

from hackernews import HackerNews

from jobs.models import Post

logger = logging.getLogger(__name__)


class Harvester(object):
    """Simple Harvester to gather hackernews posts."""

    def __init__(self, source):
        """Init the harvester with basic info."""
        self.source = source
        self.status_info = defaultdict(int)
        self.client = HackerNews()

    def harvest(self):
        """Gather some Posts from hackernews."""
        for story_id in self.client.job_stories():
            story = self.client.get_item(story_id)
            if Post.objects.filter(source=self.source, unique=story.item_id).exists():
                logger.info("HackerNews harvester got duplicate post id %s, assuming everything new is harvested.", story.item_id)
                break
            else:
                post = Post(url=story.url, source=self.source, title=story.title[:255], description=story.text, unique=story.item_id, subarea='jobs')
                self.status_info['count-job'] += 1
                self.status_info['total'] += 1
                yield post
        logger.info("HackerNews harvester status: %s", dict(self.status_info))

    def status(self):
        """Return the current status of this harvester."""
        return self.status_info

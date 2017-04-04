"""Tests related to the remotes.tasks functions."""

from django_celery_beat.models import IntervalSchedule, PeriodicTask

from jobs.models import Post
from ..models import Source
from ..tasks import setup_periodic_tasks, harvest_sources


def test_make_tasks():
    """Ensure that setup makes some tasks/schedules."""
    setup_periodic_tasks(None)
    intervals = IntervalSchedule.objects.all().count()
    tasks = PeriodicTask.objects.all().count()

    assert intervals > 0
    assert tasks > 0


def test_harvest_sources(fossjobs_rss_feed, mocker):
    """Verify that harvest sources calls harvest."""
    mocker.patch('feedparser.parse', side_effect=lambda x: fossjobs_rss_feed)
    Source.objects.all().delete()
    Source.objects.create(code='fossjobs', name='FossJobs', url='http://test.example.com/')

    pre_posts = Post.objects.all().count()
    harvest_sources()
    post_posts = Post.objects.all().count()

    assert pre_posts != post_posts
    assert post_posts > 0

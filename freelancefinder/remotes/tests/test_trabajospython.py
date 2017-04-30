"""Test the trabajospython harvester."""

from ..models import Source
from ..sources.trabajospython.trabajospython import TrabajosPython
from ..sources.trabajospython.harvest import Harvester


def test_all_jobs_returned(trabajospython_rss_feed):
    """Test that 10 jobs are returned."""
    source = Source.objects.get(code='trabajospython')
    trabajospython = TrabajosPython(source, trabajospython_rss_feed)
    all_jobs = list(trabajospython.jobs())
    assert len(all_jobs) == 10


def test_harvester(trabajospython_rss_feed, mocker):
    """Test the trabajospython harvester."""
    mocker.patch('feedparser.parse', side_effect=lambda x: trabajospython_rss_feed)
    source = Source.objects.get(code='trabajospython')
    harvester = Harvester(source)
    jobs = list(harvester.harvest())
    assert len(jobs) > 0


def test_status_info(trabajospython_rss_feed, mocker):
    """Test the trabajospython harvester counts."""
    mocker.patch('feedparser.parse', side_effect=lambda x: trabajospython_rss_feed)
    source = Source.objects.get(code='trabajospython')
    harvester = Harvester(source)
    assert harvester.status()['total'] == 0
    jobs = list(harvester.harvest())
    assert harvester.status()['total'] > 0
    assert harvester.status()['total'] == len(jobs)


def test_post_exists_does_nothing(trabajospython_rss_feed, mocker):
    """Test the fossjobs harvester stops on duplicates."""
    mocker.patch('feedparser.parse', side_effect=lambda x: trabajospython_rss_feed)
    mocker.patch('jobs.models.Post.exists', side_effect=lambda: True)
    source = Source.objects.get(code='trabajospython')
    harvester = Harvester(source)
    jobs = list(harvester.harvest())
    assert harvester.status()['total'] == 0
    assert harvester.status()['total'] == len(jobs)


def test_harvester_runs_only_once(trabajospython_rss_feed, mocker):
    """Test the fossjobs harvester has @periodically decorator."""
    mocker.patch('feedparser.parse', side_effect=lambda x: trabajospython_rss_feed)
    source = Source.objects.get(code='trabajospython')
    harvester = Harvester(source)
    jobs = list(harvester.harvest())
    assert len(jobs) > 0

    another_jobs = list(harvester.harvest())
    assert len(another_jobs) == 0

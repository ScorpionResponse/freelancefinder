"""Test the fossjobs harvester."""

from ..models import Source
from ..sources.fossjobs.fossjobs import FossJobs
from ..sources.fossjobs.harvest import Harvester


def test_all_jobs_returned(fossjobs_rss_feed):
    """Test that 10 jobs are returned."""
    source = Source.objects.get(code='fossjobs')
    fossjobs = FossJobs(source, fossjobs_rss_feed)
    all_jobs = list(fossjobs.jobs())
    assert len(all_jobs) == 10


def test_harvester(fossjobs_rss_feed, mocker):
    """Test the fossjobs harvester."""
    mocker.patch('feedparser.parse', side_effect=lambda x: fossjobs_rss_feed)
    source = Source.objects.get(code='fossjobs')
    harvester = Harvester(source)
    jobs = list(harvester.harvest())
    assert len(jobs) > 0

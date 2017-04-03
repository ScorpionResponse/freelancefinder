"""Test the fossjobs harvester."""

from ..sources.fossjobs.fossjobs import FossJobs
from ..models import Source
# from ..sources.fossjobs.harvest import Harvester


def test_all_jobs_returned(fossjobs_rss_feed):
    """Test that 10 jobs are returned."""
    source = Source.objects.get(code='fossjobs')
    fossjobs = FossJobs(source, fossjobs_rss_feed)
    all_jobs = list(fossjobs.jobs())
    assert len(all_jobs) == 10

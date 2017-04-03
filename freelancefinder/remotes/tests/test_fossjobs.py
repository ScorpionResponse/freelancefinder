"""Test the fossjobs harvester."""

from ..sources.fossjobs.fossjobs import FossJobs
from ..sources.fossjobs.harvest import Harvester


def test_all_jobs_returned(fossjobs_rss_feed):
    """Test that 10 jobs are returned."""
    fossjobs = FossJobs(fossjobs_rss_feed)
    all_jobs = list(fossjobs.jobs())
    assert len(all_jobs) == 10

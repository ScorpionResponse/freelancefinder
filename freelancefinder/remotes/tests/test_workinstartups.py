"""Test the workinstartups harvester."""

from ..models import Source
from ..sources.workinstartups.workinstartups import WorkInStartups
from ..sources.workinstartups.harvest import Harvester


def test_all_jobs_returned(workinstartups_api_response, mocker):
    """Test that 15 jobs are returned."""
    mocker.patch('requests.get', side_effect=lambda x: workinstartups_api_response)
    source = Source.objects.get(code='workinstartups')
    workinstartups = WorkInStartups(source)
    all_jobs = list(workinstartups.jobs())
    assert len(all_jobs) == 15


def test_harvester(workinstartups_api_response, mocker):
    """Test the workinstartups harvester."""
    mocker.patch('requests.get', side_effect=lambda x: workinstartups_api_response)
    source = Source.objects.get(code='workinstartups')
    harvester = Harvester(source)
    jobs = list(harvester.harvest())
    assert len(jobs) > 0


def test_status_info(workinstartups_api_response, mocker):
    """Test the workinstartups harvester counts."""
    mocker.patch('requests.get', side_effect=lambda x: workinstartups_api_response)
    source = Source.objects.get(code='workinstartups')
    harvester = Harvester(source)
    assert harvester.status()['total'] == 0
    jobs = list(harvester.harvest())
    assert harvester.status()['total'] > 0
    assert harvester.status()['total'] == len(jobs)


def test_post_exists_does_nothing(workinstartups_api_response, mocker):
    """Test the fossjobs harvester stops on duplicates."""
    mocker.patch('requests.get', side_effect=lambda x: workinstartups_api_response)
    mocker.patch('jobs.models.Post.exists', side_effect=lambda: True)
    source = Source.objects.get(code='workinstartups')
    harvester = Harvester(source)
    jobs = list(harvester.harvest())
    assert harvester.status()['total'] == 0
    assert harvester.status()['total'] == len(jobs)


def test_harvester_runs_only_once(workinstartups_api_response, mocker):
    """Test the fossjobs harvester has @periodically decorator."""
    mocker.patch('requests.get', side_effect=lambda x: workinstartups_api_response)
    source = Source.objects.get(code='workinstartups')
    harvester = Harvester(source)
    jobs = list(harvester.harvest())
    assert len(jobs) > 0

    another_jobs = list(harvester.harvest())
    assert len(another_jobs) == 0

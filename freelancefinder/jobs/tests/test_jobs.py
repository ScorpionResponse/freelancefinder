"""Tests related to Jobs functionality."""

from ..models import Job


def test_job_list(client):
    """Simple test for the jobs list page."""
    response = client.get('/jobs/job-list/')
    assert response.status_code == 200


def test_job_list_filter_search(client):
    """Test filtering job list by search field."""
    response = client.get('/jobs/job-list/?search=test')
    assert response.status_code == 200


def test_job_list_filter_tag(client):
    """Test filtering job list by tag."""
    response = client.get('/jobs/job-list/?tag=django')
    assert response.status_code == 200


def test_create_job():
    """Create a job."""
    job = Job.objects.create(title='Another New Job', description="Some Other Description")
    assert job is not None
    assert 'New Job' in str(job)

    num_jobs = Job.objects.all().count()
    assert num_jobs != 0


def test_get_jobs():
    """Ensure jobs are stored."""
    Job.objects.create(title='New Job', description="Some Description")
    num_jobs = Job.objects.all().count()
    assert num_jobs != 0

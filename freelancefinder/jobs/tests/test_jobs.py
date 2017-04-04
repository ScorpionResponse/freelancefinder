"""Tests related to Jobs functionality."""

from ..models import Job


def test_job_list(client, job, post):
    """Simple test for the jobs list page."""
    response = client.get('/jobs/job-list/')
    assert response.status_code == 200


def test_job_list_1000(client, job_factory):
    """Simple test for the jobs list page with 100 jobs."""
    for i in range(1000):
        new_job = job_factory()
    response = client.get('/jobs/job-list/')
    assert response.status_code == 200

    response = client.get('/jobs/job-list/?page=15')
    assert response.status_code == 200


def test_job_list_filter_search(client, job):
    """Test filtering job list by search field."""
    response = client.get('/jobs/job-list/?search=test')
    assert response.status_code == 200


def test_job_list_filter_tag(client, job):
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


def test_get_jobs(job):
    """Ensure jobs are stored."""
    num_jobs = Job.objects.all().count()
    assert num_jobs != 0

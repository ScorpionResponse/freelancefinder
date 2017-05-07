"""Tests related to UserJobs functionality."""

from datetime import date, datetime, timedelta

from ..models import UserJob


def test_userjob_list_302(authed_client, user_job):
    """UserJob page with no date redirects."""
    response = authed_client.get('/jobs/my-opportunities/')
    assert response.status_code == 302


def test_userjob_list_date_200(authed_client, user_job):
    """Simple test for the userjobs list page."""
    yesterday = (date.today() - timedelta(1)).strftime("%Y-%m-%d")
    response = authed_client.get('/jobs/my-opportunities/%s/' % (yesterday,))
    assert response.status_code == 200


def test_userjob_list_post_200(authed_user, authed_client, user_job_factory, post, source):
    """Simple test for the userjobs page with post."""
    yesterday = datetime.today() - timedelta(1)
    post.source = source
    post.save()
    uj = user_job_factory(job=post.job, user=authed_user, created=yesterday)
    yesterday = yesterday.strftime("%Y-%m-%d")
    response = authed_client.get('/jobs/my-opportunities/%s/' % (yesterday,))
    assert response.status_code == 200


def test_userjob_list_30(authed_user, authed_client, user_job_factory):
    """Simple test for the userjobs list page with 100 userjobs."""
    today = datetime.today()
    for i in range(30):
        new_userjob = user_job_factory(user=authed_user, job__created=today)
    today = today.strftime('%Y-%m-%d')
    response = authed_client.get('/jobs/my-opportunities/%s/' % (today,))
    assert response.status_code == 200


def test_userjob_list_filter_search(authed_client, user_job):
    """Test filtering userjob list by search field."""
    yesterday = (date.today() - timedelta(1)).strftime("%Y-%m-%d")
    response = authed_client.get('/jobs/my-opportunities/%s/?search=test' % (yesterday,))
    assert response.status_code == 200


def test_userjob_list_filter_tag(authed_client, user_job):
    """Test filtering userjob list by tag."""
    yesterday = (date.today() - timedelta(1)).strftime("%Y-%m-%d")
    response = authed_client.get('/jobs/my-opportunities/%s/?tag=django' % (yesterday,))
    assert response.status_code == 200


def test_create_userjob(job, user):
    """Create a userjob."""
    userjob = UserJob.objects.create(job=job, user=user)
    assert userjob is not None
    assert str(job) in str(userjob)
    assert str(user) in str(userjob)

    num_jobs = UserJob.objects.all().count()
    assert num_jobs != 0


def test_get_userjobs(user_job):
    """Ensure userjobs are stored."""
    num_userjobs = UserJob.objects.all().count()
    assert num_userjobs != 0

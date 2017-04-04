"""Tests related to the freelancers."""

from ..models import Freelancer


def test_freelancer_list(client, freelancer):
    """Simple test for the freelancer list page."""
    response = client.get('/jobs/freelancer-list/')
    assert response.status_code == 200


def test_freelancer_list_with_100(client, freelancer_factory):
    """Simple test for the freelancer list page."""
    for i in range(100):
        new_freelancer = freelancer_factory()
    response = client.get('/jobs/freelancer-list/')
    assert response.status_code == 200


def test_freelancer_list_search(client, freelancer):
    """Test filtering freelancer list by search field."""
    response = client.get('/jobs/freelancer-list/?search=test')
    assert response.status_code == 200


def test_freelancer_list_filter_tag(client, freelancer):
    """Test filtering freelancer list by tag."""
    response = client.get('/jobs/freelancer-list/?tag=django')
    assert response.status_code == 200


def test_create_freelancer():
    """Create a freelancer."""
    freelancer = Freelancer.objects.create(title='Another New Freelancer', description="Some Other Description")
    assert freelancer is not None
    assert 'New Freelancer' in str(freelancer)

    num_freelancers = Freelancer.objects.all().count()
    assert num_freelancers != 0


def test_get_freelancers(freelancer):
    """Test that freelancers are stored."""
    num_freelancers = Freelancer.objects.all().count()
    assert num_freelancers != 0

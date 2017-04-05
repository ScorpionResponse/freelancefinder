"""Test factory methods."""


def test_job_factory_extracted(job_factory):
    """Test the tags in the job factory."""
    job = job_factory(create_tags=['bob', 'jones'])
    assert 'bob' in job.tags.all().values_list('name', flat=True)


def test_job_factory_created(job_factory):
    """Test created does nothing."""
    job = job_factory.build(create_tags=['bob', 'jones'])
    assert job.pk is None


def test_freelancer_factory_extracted(freelancer_factory):
    """Test the tags in the freelancer factory."""
    freelancer = freelancer_factory(create_tags=['bob', 'jones'])
    assert 'bob' in freelancer.tags.all().values_list('name', flat=True)


def test_freelancer_factory_created(freelancer_factory):
    """Test created does nothing."""
    freelancer = freelancer_factory.build(create_tags=['bob', 'jones'])
    assert freelancer.pk is None

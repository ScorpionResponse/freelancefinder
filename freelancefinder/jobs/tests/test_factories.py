"""Test factory methods."""


def test_job_factory_extracted(job_factory):
    """Test the tags in the job factory."""
    job = job_factory(create_tags=['bob', 'jones'])
    assert 'bob' in job.tags.all().values_list('name', flat=True)


def test_job_factory_created(job_factory):
    """Test created does nothing."""
    job = job_factory.build(create_tags=['bob', 'jones'])
    assert job.pk is None

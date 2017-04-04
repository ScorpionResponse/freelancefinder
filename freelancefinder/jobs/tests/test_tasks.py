"""Tests for the jobs.tasks."""

from ..models import Post, Job, Freelancer
from ..tasks import process_new_posts, create_jobs, create_freelancers, tag_jobs, tag_freelancers


def test_post_processing(post_factory):
    """Verify that all posts are processed."""
    post_factory(title='[for hire] some freelancer posting', processed=False)
    post_factory(title='[hiring] some job posting', processed=False)
    pre_unprocessed_posts = Post.objects.filter(processed=False).count()
    process_new_posts()
    post_unprocessed_posts = Post.objects.filter(processed=False).count()

    assert pre_unprocessed_posts != post_unprocessed_posts
    assert post_unprocessed_posts == 0


def test_create_jobs(post_factory):
    """Verify that jobs are created."""
    post_factory(is_freelance=True, is_job_posting=True, processed=False, job=None)
    pre_jobs = Job.objects.all().count()
    create_jobs()
    post_jobs = Job.objects.all().count()

    assert post_jobs != 0
    assert pre_jobs != post_jobs


def test_create_freelancers(post_factory):
    """Verify that freelancers are created."""
    post_factory(is_freelance=True, is_freelancer=True, processed=False, freelancer=None)
    pre_freel = Freelancer.objects.all().count()
    create_freelancers()
    post_freel = Freelancer.objects.all().count()

    assert post_freel != 0
    assert pre_freel != post_freel


def test_tag_jobs(job_factory, tag_factory):
    """Verify that tags are added."""
    job = job_factory(title="Bears")
    job.tags.clear()
    job.save()
    tag_factory(name="bears")
    tag_jobs()

    changed_job = Job.objects.get(pk=job.id)
    new_tags = list(changed_job.tags.all().values_list('name', flat=True))
    assert len(new_tags) > 0
    assert 'bears' in new_tags


def test_tag_freelancers(freelancer_factory, tag_factory):
    """Verify that tags are added."""
    freelancer = freelancer_factory(title="Bores")
    freelancer.tags.clear()
    freelancer.save()
    tag_factory(name="bores")
    tag_freelancers()

    changed_freelancer = Freelancer.objects.get(pk=freelancer.id)
    new_tags = list(changed_freelancer.tags.all().values_list('name', flat=True))
    assert len(new_tags) > 0
    assert 'bores' in new_tags

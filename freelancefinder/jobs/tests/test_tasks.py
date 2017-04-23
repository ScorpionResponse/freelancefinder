"""Tests for the jobs.tasks."""

from ..models import Post, Job
from ..tasks import process_new_posts, create_jobs, tag_jobs


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
    post_factory(is_freelance=True, processed=False, job=None)
    pre_jobs = Job.objects.all().count()
    create_jobs()
    post_jobs = Job.objects.all().count()

    assert post_jobs != 0
    assert pre_jobs != post_jobs


def test_jobs_detect_dupes(post_factory):
    """Verify that duplicate detection works."""
    post_factory(title="Django Python Job", description="Lorem Ipsum Dolor", is_freelance=True, processed=False, job=None)
    create_jobs()
    pre_jobs = Job.objects.all().count()
    post_factory(title="Django Python Job", description="Lorem Ipsum Dolor", is_freelance=True, processed=False, job=None)
    create_jobs()
    post_jobs = Job.objects.all().count()

    assert post_jobs != 0
    assert pre_jobs == post_jobs


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

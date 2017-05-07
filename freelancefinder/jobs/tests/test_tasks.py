"""Tests for the jobs.tasks."""

from ..models import Post, Job, UserJob
from ..tasks import process_new_posts, create_jobs, tag_jobs, create_userjobs


def test_post_processing(post_factory):
    """Verify that all posts are processed."""
    post_factory(title='[for hire] some freelancer posting', processed=False)
    post_factory(title='[hiring] some job posting', processed=False)
    pre_unprocessed_posts = Post.objects.filter(processed=False).count()
    process_new_posts()
    post_unprocessed_posts = Post.objects.filter(processed=False).count()

    assert pre_unprocessed_posts != post_unprocessed_posts
    assert post_unprocessed_posts == 0


def test_post_processing_full_time(post_factory):
    """Verify that Full Time posts are garbaged."""
    this_post = post_factory.create(title='[Full Time] some job posting', processed=False, create_tags=['Full Time'])
    this_post.save()
    pre_unprocessed_posts = Post.objects.filter(processed=False).count()
    process_new_posts()
    post_unprocessed_posts = Post.objects.filter(processed=False).count()
    this_post = Post.all_objects.get(pk=this_post.id)

    assert pre_unprocessed_posts != post_unprocessed_posts
    assert post_unprocessed_posts == 0
    assert this_post.garbage


def test_post_processing_for_hire(post_factory):
    """Verify that For Hire posts are garbaged."""
    this_post = post_factory(title='[For Hire] some job posting', processed=False, create_tags=['For Hire'])
    this_post.save()
    pre_unprocessed_posts = Post.objects.filter(processed=False).count()
    process_new_posts()
    post_unprocessed_posts = Post.objects.filter(processed=False).count()
    this_post = Post.all_objects.get(pk=this_post.id)

    assert pre_unprocessed_posts != post_unprocessed_posts
    assert post_unprocessed_posts == 0
    assert this_post.garbage


def test_create_jobs(post_factory):
    """Verify that jobs are created."""
    post_factory(is_freelance=True, processed=False, job=None)
    pre_jobs = Job.objects.all().count()
    create_jobs()
    post_jobs = Job.objects.all().count()

    assert post_jobs != 0
    assert pre_jobs != post_jobs


def test_create_userjobs(paid_user, job):
    """Verify that UserJobs are created."""
    create_userjobs()
    assert UserJob.objects.all().count() > 0


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

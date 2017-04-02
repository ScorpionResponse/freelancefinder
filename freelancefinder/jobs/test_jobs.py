"""Tests related to jobs functionality."""

from django.test import TestCase, Client

from remotes.models import Source
from .models import Job, Post, Freelancer


def test_job_list(client):
    """Simple test for the jobs list page."""
    response = client.get('/jobs/job-list/')
    assert response.status_code == 200


def test_freelancer_list(client):
    """Simple test for the freelancer list page."""
    response = client.get('/jobs/freelancer-list/')
    assert response.status_code == 200


def test_post_list(client):
    """Simple test for the posts list page."""
    response = client.get('/jobs/post-list/')
    assert response.status_code == 200


class JobTests(TestCase):
    """Tests related to handling jobs."""

    def setUp(self):
        self.job = Job.objects.create(title='A New Job', description="Some Description")
        self.client = Client()

    def test_create_job(self):
        job = Job.objects.create(title='Another New Job', description="Some Other Description")
        num_jobs = Job.objects.all().count()
        assert num_jobs != 0
        assert job is not None
        assert 'New Job' in str(job)

    def test_get_jobs(self):
        num_jobs = Job.objects.all().count()
        assert num_jobs != 0

    def test_get_jobs_list(self):
        response = self.client.get('/jobs/job-list/')
        assert response.status_code == 200

    def tearDown(self):
        self.job.delete()


class FreelancerTests(TestCase):
    """Tests related to handling freelancers."""

    def setUp(self):
        self.freelancer = Freelancer.objects.create(title='A New Freelancer', description="Some Description")
        self.client = Client()

    def test_create_freelancer(self):
        freelancer = Freelancer.objects.create(title='Another New Freelancer', description="Some Other Description")
        num_freelancers = Freelancer.objects.all().count()
        assert num_freelancers != 0
        assert freelancer is not None
        assert 'New Freelancer' in str(freelancer)

    def test_get_freelancers(self):
        num_freelancers = Freelancer.objects.all().count()
        assert num_freelancers != 0

    def test_get_freelancers_list(self):
        response = self.client.get('/jobs/freelancer-list/')
        assert response.status_code == 200

    def tearDown(self):
        self.freelancer.delete()


class PostTests(TestCase):
    """Tests related to handling posts."""

    def setUp(self):
        self.source = Source.objects.create(code='test_source', name='Test Source', url='http://test.example.com/')
        self.job = Job.objects.create(title='A New Job', description="Some Description")
        self.post = Post.objects.create(job=self.job, url='http://www.google.com/', source=self.source,
                                        title='A New Job', description="Some Description", unique='a')
        self.client = Client()

    def test_create_post(self):
        post = Post.objects.create(job=self.job, url='http://test.example.com/', source=self.source,
                                   title='A New Post', description="Some Silly Description", unique='b')
        num_posts = Post.objects.all().count()
        assert num_posts != 0
        assert post is not None
        assert 'New Post' in str(post)

    def test_get_posts(self):
        num_jobs = Post.objects.all().count()
        assert num_jobs != 0

    def test_get_jobs_list(self):
        response = self.client.get('/jobs/post-list/')
        assert response.status_code == 200

    def tearDown(self):
        self.post.delete()
        self.job.delete()
        self.source.delete()

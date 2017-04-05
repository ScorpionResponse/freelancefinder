"""Test the reddit harvester."""

import random

from faker import Faker

from ..models import Source
from ..sources.reddit.harvest import Harvester


class PrawMock(object):
    """Mock praw.Reddit object."""

    class Submission(object):
        """Mock the submission object."""

        def __init__(self, fields):
            """Just turn dict keys into attributes."""
            for key, value in fields.items():
                setattr(self, key, value)

    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        """Just return."""
        return self

    def Reddit(self, *args, **kwargs):
        """Just return."""
        return self

    def subreddit(self, *args, **kwargs):
        """Just return."""
        return self

    def new(self, limit):
        """Return a bunch of random post like things."""
        fake = Faker()
        for times in range(limit):
            subm = {
                'url': fake.url(),
                'title': "{} {}".format(random.choice(['[HIRING]', '[FOR HIRE]', '']), fake.job()),
                'selftext': fake.text(max_nb_chars=500),
                'id': fake.uuid4(),
                'subreddit': 'fake',
                'created_utc': fake.unix_time(),
            }
            yield self.Submission(subm)


def test_harvester(mocker):
    """Test the reddit harvester."""
    mocker.patch('praw.Reddit', new_callable=PrawMock)
    source = Source.objects.get(code='reddit')
    harvester = Harvester(source)
    jobs = harvester.harvest()
    assert jobs is not None
    assert len(list(jobs)) >= 100


def test_status_info(mocker):
    """Test the reddit harvester."""
    mocker.patch('praw.Reddit', new_callable=PrawMock)
    source = Source.objects.get(code='reddit')
    harvester = Harvester(source)
    assert harvester.status()['total'] == 0
    jobs = list(harvester.harvest())
    assert harvester.status()['total'] > 0
    assert harvester.status()['total'] == len(jobs)


def test_post_exists_does_nothing(mocker):
    """Test the reddit harvester stops on duplicates."""
    mocker.patch('praw.Reddit', new_callable=PrawMock)
    mocker.patch('jobs.models.Post.exists', side_effect=lambda: True)
    source = Source.objects.get(code='reddit')
    harvester = Harvester(source)
    jobs = list(harvester.harvest())
    assert harvester.status()['total'] == 0
    assert harvester.status()['total'] == len(jobs)

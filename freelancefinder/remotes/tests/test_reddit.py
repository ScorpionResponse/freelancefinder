"""Test the reddit harvester."""

import random

from faker import Faker

from ..models import Source
from ..sources.reddit.harvest import Harvester


class PrawMock(object):

    class Submission(object):

        def __init__(self, fields):
            for k, v in fields.items():
                setattr(self, k, v)

    def __init__(self):
        pass

    def Reddit(self, *args, **kwargs):
        return self

    def subreddit(self, *args, **kwargs):
        return self

    def new(self, limit):
        fake = Faker()
        for i in range(limit):
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
    mocker.patch('praw.Reddit', spec=PrawMock)
    source = Source.objects.get(code='reddit')
    harvester = Harvester(source)
    jobs = harvester.harvest()
    assert jobs is not None

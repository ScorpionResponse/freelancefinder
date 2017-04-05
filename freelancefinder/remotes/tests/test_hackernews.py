"""Test the reddit harvester."""

import datetime

from faker import Faker
from hackernews import InvalidItemID

from ..models import Source
from ..sources.hackernews.harvest import Harvester


class HackerNewsMock(object):
    """Mock HackerNews object."""

    class Submission(object):
        """Mock the submission object."""

        def __init__(self, fields):
            """Just turn dict keys into attributes."""
            for key, value in fields.items():
                setattr(self, key, value)

    def __init__(self):
        self.cur_permutation = 0

    def __call__(self, *args, **kwargs):
        """Just return."""
        return self

    def get_user(self, *args, **kwargs):
        """Just return."""
        return self

    @property
    def submitted(self, *args, **kwargs):
        """Just return."""
        return [1, 2, 3]

    def job_stories(self, limit):
        return range(4, limit)

    def get_item(self, item_id):
        """Return a thing like a HN comment."""
        fake = Faker()
        subm = {
            'url': fake.url(),
            'title': fake.job(),
            'text': fake.text(max_nb_chars=500),
            'by': fake.name(),
            'item_id': fake.uuid4(),
            'submission_time': fake.date_time(tzinfo=None),
            'kids': range(20),
        }
        month_year = datetime.date.today().strftime("%B %Y")
        item_id = int(item_id)
        if item_id == 1:
            subm['title'] = 'Who is hiring? ({})'.format(month_year)
        elif item_id == 2:
            subm['title'] = 'Freelancer? Seeking freelancer? ({})'.format(month_year)
        elif item_id == 3:
            subm['title'] = 'Who wants to be hired? ({})'.format(month_year)
        else:
            self.cur_permutation += 1
            if self.cur_permutation == 1:
                subm['title'] = None
            elif self.cur_permutation == 2:
                subm['url'] = None
            elif self.cur_permutation == 3:
                subm['text'] = None
            elif self.cur_permutation == 4:
                raise InvalidItemID('you broke it')
            elif self.cur_permutation == 5:
                subm['title'] = 'SEEKING WORK ' + subm['title']
            elif self.cur_permutation == 6:
                subm['title'] = 'SEEKING FREELANCER ' + subm['title']
            elif self.cur_permutation < 12:
                pass
            else:
                self.cur_permutation = 0

        return self.Submission(subm)


def test_harvester(mocker):
    """Test the reddit harvester."""
    mocker.patch('hackernews.HackerNews', new_callable=HackerNewsMock)
    source = Source.objects.get(code='hackernews')
    harvester = Harvester(source)
    jobs = harvester.harvest()
    assert jobs is not None
    assert len(list(jobs)) >= 100


def test_status_info(mocker):
    """Test the reddit harvester."""
    mocker.patch('hackernews.HackerNews', new_callable=HackerNewsMock)
    source = Source.objects.get(code='hackernews')
    harvester = Harvester(source)
    assert harvester.status()['total'] == 0
    jobs = list(harvester.harvest())
    assert harvester.status()['total'] > 0
    assert harvester.status()['total'] == len(jobs)


def test_post_exists_does_nothing(mocker):
    """Test the reddit harvester stops on duplicates."""
    mocker.patch('hackernews.HackerNews', new_callable=HackerNewsMock)
    mocker.patch('jobs.models.Post.exists', side_effect=lambda: True)
    source = Source.objects.get(code='hackernews')
    harvester = Harvester(source)
    jobs = list(harvester.harvest())
    assert harvester.status()['total'] == 0
    assert harvester.status()['total'] == len(jobs)


def test_calling_twice_does_nothing(mocker):
    """Test the reddit harvester stops on duplicates."""
    mocker.patch('hackernews.HackerNews', new_callable=HackerNewsMock)
    source = Source.objects.get(code='hackernews')
    harvester = Harvester(source)
    jobs = list(harvester.harvest())
    num_jobs = len(jobs)
    assert harvester.status()['total'] > 0
    assert harvester.status()['total'] == num_jobs
    new_jobs = harvester.harvest()
    num_new_jobs = len(list(new_jobs))
    assert num_new_jobs == 0
    assert harvester.status()['total'] == num_jobs

# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-17 09:51
from __future__ import unicode_literals

from django.db import migrations

NEW_SOURCES = [
    {'code': 'remotepython', 'name': 'Remote Python', 'url': 'https://www.remotepython.com/', 'harvest_type': 'rss_feed', 'config': {'config_key': 'rss_feed_address', 'config_value': 'https://www.remotepython.com/latest/jobs/feed/'}},
    {'code': 'startupjobsasia', 'name': 'StartUpJobs Asia', 'url': 'http://startupjobs.asia/', 'harvest_type': 'rss_feed', 'config': {'config_key': 'rss_feed_address', 'config_value': 'http://startupjobs.asia/feed/'}},
    {'code': 'freelancezonesg', 'name': 'FreelanceZone.com.sg', 'url': 'https://www.freelancezone.com.sg/', 'harvest_type': 'rss_feed', 'config': {'config_key': 'rss_feed_address', 'config_value': 'https://www.freelancezone.com.sg/makeRssFeeds'}},
    {'code': 'djangojobs', 'name': 'DjangoJobs', 'url': 'https://djangojobs.net/jobs/', 'harvest_type': 'rss_feed', 'config': {'config_key': 'rss_feed_address', 'config_value': 'https://djangojobs.net/jobs/latest/feed/rss/'}},
    {'code': 'djangogigs', 'name': 'Djangogigs', 'url': 'https://djangogigs.com/', 'harvest_type': 'rss_feed', 'config': {'config_key': 'rss_feed_address', 'config_value': 'https://djangogigs.com/feeds/gigs/'}},
    {'code': 'pythonjobs', 'name': 'Python Job Board', 'url': 'https://www.python.org/jobs/', 'harvest_type': 'rss_feed', 'config': {'config_key': 'rss_feed_address', 'config_value': 'https://www.python.org/jobs/feed/rss/'}},
    {'code': 'pythonjobs_github', 'name': 'Free Python Job Board', 'url': 'http://pythonjobs.github.io/', 'harvest_type': 'rss_feed', 'config': {'config_key': 'rss_feed_address', 'config_value': 'http://pythonjobs.github.io/atom.xml'}},
    {'code': 'pythonjobs_hq', 'name': 'Python Jobs HQ', 'url': 'http://www.pythonjobshq.com/', 'harvest_type': 'rss_feed', 'config': {'config_key': 'rss_feed_address', 'config_value': 'http://www.pythonjobshq.com/jobs.atom'}},
    {'code': 'stackoverflow', 'name': 'StackOverflow Jobs', 'url': 'http://stackoverflow.com/jobs/', 'harvest_type': 'rss_feed', 'config': {'config_key': 'rss_feed_address', 'config_value': 'http://stackoverflow.com/jobs/feed'}},
]


def load_sources(apps, schema_editor):
    '''Load new source data.'''
    frequency_config = {'config_key': 'frequency', 'config_value': 'daily'}
    Source = apps.get_model('remotes', 'Source')
    for source in NEW_SOURCES:
        config_data = source['config']
        del source['config']
        new_source = Source(**source)
        new_source.save()
        new_source.config.create(**config_data)
        new_source.config.create(**frequency_config)


def delete_sources(apps, schema_editor):
    '''Delete source data.'''
    Source = apps.get_model('remotes', 'Source')
    for source in NEW_SOURCES:
        Source.objects.filter(code=source['code']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0008_source_harvest_type'),
    ]

    operations = [
        migrations.RunPython(load_sources, reverse_code=delete_sources),
    ]

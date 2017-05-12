# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-30 18:30
from __future__ import unicode_literals

from django.db import migrations

NEW_SOURCES = [
    {'code': 'trabajospython', 'name': 'Trabajos Python', 'url': 'http://www.trabajospython.com/'},
    {'code': 'workinstartups', 'name': 'Work In Startups', 'url': 'http://workinstartups.com/'},
    {'code': 'workingnomads', 'name': 'Working Nomads', 'url': 'https://www.workingnomads.co/'},
]


def load_sources(apps, schema_editor):
    '''Load new source data.'''
    Source = apps.get_model('remotes', 'Source')
    for source in NEW_SOURCES:
        new_source = Source(**source)
        new_source.save()


def delete_sources(apps, schema_editor):
    '''Delete source data.'''
    Source = apps.get_model('remotes', 'Source')
    for source in NEW_SOURCES:
        Source.objects.filter(code=source['code']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0006_auto_20170425_0911'),
    ]

    operations = [
        migrations.RunPython(load_sources, reverse_code=delete_sources),
    ]

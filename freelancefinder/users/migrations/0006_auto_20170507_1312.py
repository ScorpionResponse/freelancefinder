# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-07 13:12
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20170505_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='refresh_frequency',
            field=models.CharField(choices=[('daily', 'Daily'), ('twice_a_day', 'Twice a Day'), ('hourly', 'Hourly')], default='daily', max_length=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]

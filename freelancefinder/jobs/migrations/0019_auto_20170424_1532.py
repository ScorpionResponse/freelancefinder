# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 15:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0018_remove_post_is_job_posting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tagvariant',
            name='id',
        ),
        migrations.AlterField(
            model_name='tagvariant',
            name='variant',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]
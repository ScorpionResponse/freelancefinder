# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-04 17:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_auto_20170301_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='subarea',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
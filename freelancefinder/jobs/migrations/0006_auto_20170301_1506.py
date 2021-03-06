# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 15:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_auto_20170223_1350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='date_added',
        ),
        migrations.AddField(
            model_name='job',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='job',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
        migrations.AddField(
            model_name='post',
            name='processed',
            field=models.BooleanField(default=False),
        ),
    ]

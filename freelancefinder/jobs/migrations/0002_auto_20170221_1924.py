# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 19:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='jobs.Job'),
        ),
    ]
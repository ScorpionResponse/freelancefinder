# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 15:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0004_auto_20170222_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='code',
            field=models.CharField(max_length=40, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='sourceconfig',
            name='config_key',
            field=models.CharField(max_length=100),
        ),
    ]
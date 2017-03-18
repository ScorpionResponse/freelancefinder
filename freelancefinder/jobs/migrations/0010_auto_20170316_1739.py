# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-16 17:39
from __future__ import unicode_literals

from django.db import migrations

TAGS = {
    '.NET': [],
    'ASP.NET': [],
    'Android': [],
    'AngularJS': ['angular.js', 'angular'],
    'Ansible': [],
    'Bootstrap': [],
    'Chef': [],
    'Contract': [],
    'Copywriting': ['copywriter'],
    'DevOps': [],
    'Django': [],
    'Full Time': ['full-time', 'fulltime'],
    'GoLang': [],
    'Javascript': ['js'],
    'Marketing': ['marketer'],
    'MongoDB': ['mongo'],
    'MySQL': [],
    'Node.js': ['node'],
    'PHP': [],
    'Part Time': ['part-time', 'parttime'],
    'PostgreSQL': [],
    'Product Manager': [],
    'Project Manager': [],
    'Puppet': [],
    'Python': [],
    'Rails': [],
    'React.js': ['react'],
    'Ruby': [],
    'SEO': [],
    'Sales': [],
    'Social Media': [],
    'Video': [],
    'Web Design': ['web designer'],
    'WordPress': [],
    'iOS': [],
    'jQuery': ['j-query'],
    'scraping': ['scraper', 'scrape'],
}


def load_tags(apps, schema_editor):
    """Load new tags."""
    from taggit.models import Tag
    from jobs.models import TagVariant
    for tag in TAGS:
        new_tag, created = Tag.objects.get_or_create(name=tag)
        for variant in TAGS[tag]:
            TagVariant.objects.get_or_create(variant=variant, tag=new_tag)


def delete_tags(apps, schema_editor):
    """Remove all tags and variants."""
    Tag = apps.get_model('taggit', 'Tag')
    TagVariant = apps.get_model('jobs', 'TagVariant')

    TagVariant.objects.all().delete()
    Tag.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0009_tagvariant'),
    ]

    operations = [
        migrations.RunPython(load_tags, reverse_code=delete_tags),
    ]
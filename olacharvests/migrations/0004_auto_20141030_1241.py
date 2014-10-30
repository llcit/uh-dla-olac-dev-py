# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olacharvests', '0003_auto_20141030_0944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repository',
            name='access',
        ),
        migrations.RemoveField(
            model_name='repository',
            name='archive_url',
        ),
        migrations.RemoveField(
            model_name='repository',
            name='datestamp',
        ),
        migrations.RemoveField(
            model_name='repository',
            name='institution',
        ),
        migrations.RemoveField(
            model_name='repository',
            name='institution_url',
        ),
        migrations.RemoveField(
            model_name='repository',
            name='location',
        ),
        migrations.RemoveField(
            model_name='repository',
            name='participants',
        ),
        migrations.RemoveField(
            model_name='repository',
            name='short_location',
        ),
        migrations.RemoveField(
            model_name='repository',
            name='submission_policy',
        ),
        migrations.RemoveField(
            model_name='repository',
            name='synopsis',
        ),
        migrations.AddField(
            model_name='repository',
            name='info_list',
            field=models.TextField(default={}, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repository',
            name='base_url',
            field=models.CharField(unique=True, max_length=1024),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repository',
            name='name',
            field=models.CharField(unique=True, max_length=512),
            preserve_default=True,
        ),
    ]

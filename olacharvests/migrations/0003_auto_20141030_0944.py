# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olacharvests', '0002_auto_20141030_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='access',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repository',
            name='archive_url',
            field=models.CharField(max_length=512, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repository',
            name='base_url',
            field=models.CharField(max_length=512, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repository',
            name='datestamp',
            field=models.CharField(max_length=64, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repository',
            name='institution',
            field=models.CharField(max_length=512, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repository',
            name='institution_url',
            field=models.CharField(max_length=512, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repository',
            name='location',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repository',
            name='name',
            field=models.CharField(max_length=512),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repository',
            name='short_location',
            field=models.CharField(max_length=512, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repository',
            name='submission_policy',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repository',
            name='synopsis',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]

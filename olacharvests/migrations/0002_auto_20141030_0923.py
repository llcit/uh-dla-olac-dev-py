# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olacharvests', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='datestamp',
            field=models.DateField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repository',
            name='participants',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olacharvests', '0004_repository_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='slug',
            field=models.SlugField(null=True),
            preserve_default=True,
        ),
    ]

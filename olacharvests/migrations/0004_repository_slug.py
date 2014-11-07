# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olacharvests', '0003_repository_last_harvest'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='slug',
            field=models.SlugField(default=2, blank=True),
            preserve_default=False,
        ),
    ]

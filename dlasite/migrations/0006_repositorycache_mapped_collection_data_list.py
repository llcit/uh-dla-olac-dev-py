# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dlasite', '0005_auto_20141105_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='repositorycache',
            name='mapped_collection_data_list',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
    ]

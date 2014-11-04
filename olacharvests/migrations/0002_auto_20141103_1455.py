# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olacharvests', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metadataelement',
            name='element_data',
            field=models.TextField(default=b'', null=True),
            preserve_default=True,
        ),
    ]

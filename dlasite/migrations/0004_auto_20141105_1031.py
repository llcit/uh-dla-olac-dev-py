# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dlasite', '0003_auto_20141105_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repositoryregistration',
            name='last_harvest',
            field=models.DateField(blank=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olacharvests', '0002_auto_20141103_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='last_harvest',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
    ]

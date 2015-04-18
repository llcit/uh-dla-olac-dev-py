# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olacharvests', '0011_auto_20150417_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='slug',
            field=models.SlugField(max_length=512, null=True),
            preserve_default=True,
        ),
    ]

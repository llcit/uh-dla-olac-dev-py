# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olacharvests', '0006_collection_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='datestamp',
            new_name='datestampstr',
        ),
    ]

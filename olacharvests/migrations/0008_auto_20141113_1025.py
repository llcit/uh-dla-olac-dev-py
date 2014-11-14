# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olacharvests', '0007_auto_20141113_1022'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='datestampstr',
            new_name='datestamp',
        ),
    ]

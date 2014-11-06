# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dlasite', '0004_auto_20141105_1031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repositoryregistration',
            name='repository',
        ),
        migrations.DeleteModel(
            name='RepositoryRegistration',
        ),
    ]

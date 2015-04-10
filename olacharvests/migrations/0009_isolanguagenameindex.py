# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olacharvests', '0008_auto_20141113_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='ISOLanguageNameIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=3)),
                ('print_name', models.CharField(max_length=75)),
                ('inverted_name', models.CharField(max_length=75, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

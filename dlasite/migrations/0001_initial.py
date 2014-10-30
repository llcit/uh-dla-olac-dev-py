# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olacharvests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepositoryCache',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_list', models.TextField(blank=True)),
                ('contributor_list', models.TextField(blank=True)),
                ('mapped_data_list', models.TextField(blank=True)),
                ('repository', models.ForeignKey(blank=True, to='olacharvests.Repository', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

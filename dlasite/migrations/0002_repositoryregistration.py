# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olacharvests', '0002_auto_20141103_1455'),
        ('dlasite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepositoryRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_harvest', models.DateField()),
                ('repository', models.ForeignKey(to='olacharvests.Repository', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

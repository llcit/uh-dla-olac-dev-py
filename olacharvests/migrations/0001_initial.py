# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('identifier', models.CharField(max_length=256, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MetadataElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('element_type', models.CharField(max_length=256)),
                ('element_data', models.TextField(default=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('identifier', models.CharField(unique=True, max_length=256)),
                ('datestamp', models.DateTimeField()),
                ('set_spec', models.ForeignKey(to='olacharvests.Collection')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=256)),
                ('datestamp', models.DateTimeField()),
                ('base_url', models.URLField(unique=True)),
                ('archive_url', models.URLField(unique=True)),
                ('participants', models.TextField()),
                ('institution', models.CharField(max_length=256)),
                ('institution_url', models.URLField()),
                ('short_location', models.CharField(max_length=512)),
                ('location', models.CharField(max_length=512)),
                ('synopsis', models.TextField()),
                ('access', models.TextField()),
                ('submission_policy', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='metadataelement',
            name='record',
            field=models.ForeignKey(related_name='data', to='olacharvests.Record', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collection',
            name='repository',
            field=models.ForeignKey(blank=True, to='olacharvests.Repository', null=True),
            preserve_default=True,
        ),
    ]

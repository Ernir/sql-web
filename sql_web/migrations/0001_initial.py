# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('identifier', models.CharField(max_length=50, unique=True)),
                ('code', models.TextField()),
                ('description', models.TextField()),
                ('programming_language', models.CharField(default='sql', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('identifier', models.CharField(max_length=50, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('problem_description', models.TextField()),
                ('given_schema', models.TextField()),
                ('sql_to_emulate', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('html_contents', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='section',
            name='subject',
            field=models.ForeignKey(to='sql_web.Subject'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='section',
            field=models.ManyToManyField(to='sql_web.Section'),
        ),
    ]

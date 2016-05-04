# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-04 17:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sql_web', '0018_section_rendered_contents'),
    ]

    operations = [
        migrations.CreateModel(
            name='Footnote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=50)),
                ('raw_contents', models.TextField()),
                ('rendered_contents', models.TextField()),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sql_web.Section')),
            ],
        ),
    ]

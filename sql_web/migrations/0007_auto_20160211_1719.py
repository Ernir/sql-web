# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-11 17:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sql_web', '0006_figure'),
    ]

    operations = [
        migrations.RenameField(
            model_name='figure',
            old_name='description',
            new_name='full_description',
        ),
        migrations.RemoveField(
            model_name='figure',
            name='title',
        ),
        migrations.AddField(
            model_name='figure',
            name='short_description',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]

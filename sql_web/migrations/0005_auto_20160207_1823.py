# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-07 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sql_web', '0004_section_connected_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='connected_to',
            field=models.ManyToManyField(blank=True, related_name='_section_connected_to_+', to='sql_web.Section'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-30 11:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sql_web', '0022_footnote_section'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='figure',
            name='short_description',
        ),
    ]

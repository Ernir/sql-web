# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-03 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sql_web', '0030_course_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='rendered_description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
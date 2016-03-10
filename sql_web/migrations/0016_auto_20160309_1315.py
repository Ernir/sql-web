# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-09 13:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sql_web', '0015_section_read_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='read_by',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
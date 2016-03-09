# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-09 13:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sql_web', '0014_auto_20160303_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='read_by',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]

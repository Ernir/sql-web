# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-09-03 20:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sql_web', '0044_auto_20160818_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='assignments',
        ),
        migrations.AlterField(
            model_name='assignment',
            name='assigned_students',
            field=models.ManyToManyField(blank=True, help_text='Setja verkefni fyrir einstaka nemendur', to=settings.AUTH_USER_MODEL),
        ),
    ]

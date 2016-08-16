# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-12 17:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sql_web', '0040_section_good_start'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='good_start',
        ),
        migrations.AddField(
            model_name='subject',
            name='best_start',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='considered_best_start_by', to='sql_web.Section'),
        ),
    ]
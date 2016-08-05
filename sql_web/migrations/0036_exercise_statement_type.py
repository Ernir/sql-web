# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-05 11:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sql_web', '0035_section_associated_exercises'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='statement_type',
            field=models.CharField(choices=[('DDL', 'DDL'), ('DML', 'DML')], default='DML', max_length=3),
        ),
    ]

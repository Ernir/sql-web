# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-06 12:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sql_web', '0026_auto_20160606_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='number',
            field=models.IntegerField(unique=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sql_web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='identifier',
            field=models.CharField(max_length=50, unique=True, default='1.2.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='section',
            name='title',
            field=models.CharField(max_length=200, default='Hvað er gagnagrunnur?'),
            preserve_default=False,
        ),
    ]

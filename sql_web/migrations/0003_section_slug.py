# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sql_web', '0002_auto_20151015_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='slug',
            field=models.SlugField(default='bad-slug'),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-02 18:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sql_web', '0028_auto_20160726_1538'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('open_to_all', models.BooleanField(default=True, help_text='Sé áfanginn lokaður sérð þú um að skrá inn nemendur')),
                ('assignments', models.ManyToManyField(blank=True, to='sql_web.Assignment')),
                ('members', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

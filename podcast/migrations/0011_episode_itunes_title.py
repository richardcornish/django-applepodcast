# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-23 02:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0010_auto_20170923_0131'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='itunes_title',
            field=models.CharField(blank=True, help_text='Do not specify show title, episode number, or season number; if blank, uses original title', max_length=255, verbose_name='title'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 21:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0022_remove_category_json'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='show',
            name='itunes',
        ),
        migrations.AddField(
            model_name='show',
            name='apple',
            field=models.URLField(blank=True, help_text='Paste Apple Podcasts URL here after submission of show feed URL to <a href="https://podcastsconnect.apple.com/">Podcasts Connect</a>', verbose_name='Apple Podcasts URL'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='block',
            field=models.BooleanField(default=False, help_text='Prevents episode from appearing on Apple Podcasts', verbose_name='block?'),
        ),
        migrations.AlterField(
            model_name='show',
            name='block',
            field=models.BooleanField(default=False, help_text='Prevents entire podcast from appearing on Apple Podcasts', verbose_name='block?'),
        ),
    ]

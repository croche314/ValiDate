# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 20:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dating_app', '0008_match_percent_match'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='about_you',
            field=models.TextField(default='hello', max_length=1000),
            preserve_default=False,
        ),
    ]

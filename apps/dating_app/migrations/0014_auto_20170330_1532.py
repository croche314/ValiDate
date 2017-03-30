# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-30 15:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dating_app', '0013_auto_20170329_2200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='user1',
        ),
        migrations.RemoveField(
            model_name='like',
            name='user2',
        ),
        migrations.AddField(
            model_name='like',
            name='like1',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='liker', to='dating_app.User'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='like',
            name='like2',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='likee', to='dating_app.User'),
            preserve_default=False,
        ),
    ]
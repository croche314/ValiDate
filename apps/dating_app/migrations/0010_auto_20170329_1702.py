# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-29 17:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dating_app', '0009_answer_about_you'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='my_answers', to='dating_app.User'),
        ),
    ]

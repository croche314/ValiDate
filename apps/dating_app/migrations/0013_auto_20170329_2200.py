# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-29 22:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dating_app', '0012_auto_20170329_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='my_pic', to='dating_app.User'),
        ),
        migrations.AlterField(
            model_name='image',
            name='user_pic',
            field=models.FileField(default='img/user.png', upload_to='img'),
        ),
    ]

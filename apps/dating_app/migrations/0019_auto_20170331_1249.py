# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-31 12:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dating_app', '0018_auto_20170331_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='conversation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='dating_app.Conversation'),
        ),
    ]

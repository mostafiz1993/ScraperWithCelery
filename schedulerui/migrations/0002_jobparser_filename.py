# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-03-06 11:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedulerui', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobparser',
            name='fileName',
            field=models.CharField(max_length=200, null=True),
        ),
    ]

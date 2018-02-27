# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-02-19 09:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djcelery', '0001_initial'),
        ('testapp', '0005_jobinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskScheduler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('periodic_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djcelery.PeriodicTask')),
            ],
        ),
    ]
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class SITE(models.Model):
    name    = models.CharField(max_length=15)
    job_title = models.CharField(max_length=50)
    location = models.CharField(max_length=30)
    company_name = models.CharField(max_length=50)
    recurrence = models.CharField(max_length=5)
    seach_start_time  = models.DateTimeField()
    until_stop = models.IntegerField()
# Create your models here.

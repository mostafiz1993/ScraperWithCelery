# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class SITE(models.Model):
    name    = models.CharField(max_length=15)
    job_title = models.CharField(max_length=50,blank=True,null = True)
    location = models.CharField(max_length=30,blank=True,null = True)
    company_name = models.CharField(max_length=50,blank=True,null = True)
    recurrence = models.CharField(max_length=5,blank=True,null = True)
    search_start_time  = models.DateTimeField(blank=True,null = True)
    #until_stop = models.IntegerField()
# Create your models here.

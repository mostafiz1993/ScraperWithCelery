# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class SITE(models.Model):
    name    = models.CharField(max_length=15)
    job_title = models.CharField(max_length=50,blank=True,null = True)
    location = models.CharField(max_length=30,blank=True,null = True)
    company_name = models.CharField(max_length=50,blank=True,null = True)
    recurrence = models.CharField(max_length=5,blank=True,null = True)
    search_start_time  = models.DateTimeField(blank=True,null = True)
    #until_stop = models.IntegerField()

# Create your models here.

class JobParser(models.Model):
    siteName = models.CharField(max_length=200, blank=False)
    siteURL = models.CharField(max_length=200, blank=False)
    searchSyntax = models.CharField(max_length=200, blank=True, null = True)
    jobTitle = models.CharField(max_length=200, blank=True, null = True)
    location = models.CharField(max_length=200, blank=True, null = True)

    # jobCategory = models.CharField(max_length=200, blank=True, null = True)
    # city = models.CharField(max_length=200, blank=True, null = True)
    # state = models.CharField(max_length=200, blank=True, null = True)
    # country = models.CharField(max_length=200, blank=True, null = True)
    # zipcode = models.CharField(max_length=200, blank=True, null = True)
    # salaryInfo = models.CharField(max_length=200, blank=True, null = True)
    # yearsOfExp = models.CharField(max_length=200, blank=True, null = True)
    # jobPostedDate = models.CharField(max_length=200, blank=True, null = True)
    # companyName = models.CharField(max_length=200, blank=True, null = True)
    # companyDomainAddress = models.CharField(max_length=200, blank=True, null = True)
    # jobURL = models.CharField(max_length=200, blank=True, null = True)
    # jobDesc = models.CharField(max_length=200, blank=True, null = True)
    # aboutCompany = models.CharField(max_length=200, blank=True, null = True)
    # numOfJob = models.CharField(max_length=200, blank=True, null = True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)


class JobScheduler(models.Model):
    siteURL = models.CharField(max_length=200, blank=False)
    jobTitle = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)

    jobId = models.CharField(null=False, max_length=300, blank=False)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    recurrence = models.CharField(default="Daily", max_length=300, blank=False)
    status = models.CharField(max_length=5,default='PENDING')

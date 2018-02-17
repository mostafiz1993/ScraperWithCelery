from django.db import models
from django.utils import timezone
# Create your models here.
class Calcu(models.Model):
    n = models.CharField(max_length=10)


class JobInfo(models.Model):
    jobName = models.CharField(null=False,max_length=300)
    jobId = models.CharField(null=False, max_length=300)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=5,default='PENDING')
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from celery.result import AsyncResult
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render, redirect
import json
from .forms import *
from .models import *
import requests
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .scheduledTask import *
from django.utils import timezone
from datetime import datetime

@login_required(login_url='/home/index/')
def addParserJob(request):
    if request.method == "POST":
        form = JobParserFrom(request.POST)
        if form.is_valid():
            siteName = form.cleaned_data['siteName']
            siteURL = form.cleaned_data['siteURL']
            searchSyntax = form.cleaned_data['searchSyntax']
            #jobTitle = form.cleaned_data['jobTitle']
            #location = form.cleaned_data['location']
            jobParser = JobParser.objects.create(siteName=siteName,siteURL=siteURL,searchSyntax=searchSyntax)
            jobParser.save()
            # print(siteName)
            # print(siteURL)
            # print(searchSyntax)
            form = JobParserFrom()
            jobParserListJson = getAllJobParser()
            return render(request, 'newJobParser.html', {"form": form, "jobParserListJson": json.loads(jobParserListJson)})

    else:
        form = JobParserFrom()

    jobParserListJson = getAllJobParser()
    return render(request, 'newJobParser.html', {"form":form, "jobParserListJson": json.loads(jobParserListJson)})


def index(request):
    print(request.user)
    if request.user.is_authenticated:
        #print("auth")
        if request.method == "POST":
            form = JobParserFrom(request.POST)
            if form.is_valid():
                siteName = form.cleaned_data['siteName']
                siteURL = form.cleaned_data['siteURL']
                searchSyntax = form.cleaned_data['searchSyntax']
                #jobTitle = form.cleaned_data['jobTitle']
                #location = form.cleaned_data['location']
                jobParser = JobParser.objects.create(siteName=siteName, siteURL=siteURL, searchSyntax=searchSyntax)
                jobParser.save()
                form = JobParserFrom()
                jobParserListJson = getAllJobParser()
                return render(request, 'newJobParser.html',
                              {"form": form, "jobParserListJson": json.loads(jobParserListJson)})

        else:
            form = JobParserFrom()

        jobParserListJson = getAllJobParser()
        return render(request, 'newJobParser.html', {"form": form, "jobParserListJson": json.loads(jobParserListJson)})
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data['userName']
                password = form.cleaned_data['password']
                auth = requests.post("http://api.raasforce.com/Token","grant_type=password&username=" + user +"&password=" + password)
                content = auth.json()
                accessToken = ""
                for k,v in content.items():
                    if(k == "access_token"):
                        accessToken = v

                if accessToken != "":
                    print("login success")
                    form = JobParserFrom()
                    jobParserListJson = getAllJobParser()
                    if not (User.objects.filter(username=user).exists() or User.objects.filter(email=user).exists()):
                        User.objects.create_user(user, user, password)
                    user = authenticate(username=user, password=password)
                    login(request, user)
                    return render(request, 'newJobParser.html',
                                  {"form": form, "jobParserListJson": json.loads(jobParserListJson)})
                else:
                    print("login fail")
                    loginForm = LoginForm()
                    return render(request,'index.html',{'form' : loginForm})

        loginForm = LoginForm()
        return render(request,'index.html',{'form' : loginForm})


def logout_view(request):
    logout(request)
    #loginForm = LoginForm()
    return render(request, 'logout.html')

def getAllJobParser():
    jobParserList = JobParser.objects.all()
    results = []
    for jobParser in jobParserList:
        jobParserJson = {}
        jobParserJson['siteName'] = jobParser.siteName
        jobParserJson['siteURL'] = jobParser.siteURL
        #jobParserJson['jobTitle'] = jobParser.jobTitle
        jobParserJson['jobId'] = jobParser.id
        jobParserJson['created'] = jobParser.created.strftime("%d-%m-%Y")
        results.append(jobParserJson)
    jobParserListJson = json.dumps(results)
    return jobParserListJson

def calculateFirstTime(hour):
    currDate = datetime.now().strftime("%Y-%m-%d")
    newTime = currDate + " " + str(hour)
    newTimeObj = datetime.strptime(newTime, "%Y-%m-%d %H")

    currTime = datetime.now()
    diff = newTimeObj - currTime

    if diff.seconds >= 0:
        return diff.seconds
    else:
        return -1

def calculateSecondTime(period):
    scriptRunTime = 30*60
    if period==1: #daily
        return (24*3600 - scriptRunTime)
    elif period == 2: #two day
        return (2 * 24 * 3600 - scriptRunTime)
    elif period == 3: #weekly
        return (7 * 24 * 3600 - scriptRunTime)
    else: #monthly
        return (30 * 24 * 3600 - scriptRunTime)

def getStateByJobId(jobId):
    job = AsyncResult(jobId)
    return job.state

def revokeJobByJobId(jobId):
    from celery import app
    app.control.revoke(jobId)

def killJobByJobId(jobId):
    try:
        job = AsyncResult(jobId)
        job.revoke(terminate=True)
        return True
    except:
        return False

def addJobInScheduler(request):
    if request.method == "POST":
        form = JobSchedulerForm(request.POST)
        if form.is_valid():
            siteURL = form.cleaned_data['siteURL']
            jobTitle = form.cleaned_data['jobTitle']
            location = form.cleaned_data['location']
            recurrence = form.cleaned_data['recurrence']
            oneTimeProcess = form.cleaned_data['oneTimeProcess']
            dailyStartTime = form.cleaned_data['startingHour']

            firstTime = calculateFirstTime(dailyStartTime)

            if(oneTimeProcess):
                secondTime = -1
                job = taskState.apply_async(args=[firstTime,secondTime], countdown=1)
                state = job.state
                jobScheduler = JobScheduler.objects.create(siteURL=siteURL, jobTitle=jobTitle, location=location,
                                                           recurrence=recurrence,jobId=job.id,status=state)
                jobScheduler.save()
            else:
                secondTime = calculateSecondTime(recurrence)
                job = taskState.apply_async(args=[firstTime, secondTime], countdown=1)
                state = job.state
                jobScheduler = JobScheduler.objects.create(siteURL=siteURL, jobTitle=jobTitle, location=location,
                                                           recurrence=recurrence, jobId=job.id, status=state)

                jobScheduler.save()

            print(oneTimeProcess)
            print(dailyStartTime)

            form = JobSchedulerForm()
            scheduledJobListJson = getAllScheduledJob()
            return render(request, 'jobScheduler.html',
                          {"form": form, "scheduledJobListJson": json.loads(scheduledJobListJson)})

    else:
        form = JobSchedulerForm()
        scheduledJobListJson = getAllScheduledJob()
        return render(request, 'jobScheduler.html',
                      {"form": form, "scheduledJobListJson": json.loads(scheduledJobListJson)})

    return render(request, 'jobScheduler.html', {"form": form})

def getAllScheduledJob():
    jobSchedulerList = JobScheduler.objects.all()
    results = []
    for scheduledJobRow in jobSchedulerList:
        scheduledJob = {}
        scheduledJob['siteURL'] = scheduledJobRow.siteURL
        scheduledJob['jobTitle'] = scheduledJobRow.jobTitle
        scheduledJob['jobId'] = scheduledJobRow.id
        status = getStateByJobId(scheduledJobRow.jobId)

        if (status != scheduledJobRow.status):
            JobScheduler.objects.filter(jobId=scheduledJobRow.jobId).update(status=status,updated=timezone.now())

        scheduledJob['status'] = status
        scheduledJob['created'] = scheduledJobRow.created.strftime("%d-%m-%Y")

        results.append(scheduledJob)
    jobSchedulerListJson = json.dumps(results)
    return jobSchedulerListJson

def deleteJobParser(request,jobparserid):
    print(jobparserid)
    jobParser = JobParser.objects.get(pk=jobparserid)
    jobParser.delete()
    return redirect("/home/addparserjob")

def deleteJobScheduler(request,jobschedulerid):
    print(jobschedulerid)
    jobScheduler = JobScheduler.objects.get(pk=jobschedulerid)
    killJobByJobId(jobScheduler.jobId)
    jobScheduler.delete()
    return redirect("/home/addjobinscheduler")


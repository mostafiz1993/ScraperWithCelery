from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from testapp.models import JobInfo, TaskScheduler
from .forms import UserForm, JobForm
from .tasks import *
from celery.result import AsyncResult
import json

# Create your views here.
def poll_state(request):
    """ A view to report the progress to the user """
    data = 'Fail'
    if request.is_ajax():
        if 'task_id' in request.POST.keys() and request.POST['task_id']:
            task_id = request.POST['task_id']
            task = AsyncResult(task_id)
            data = task.result or task.state
        else:
            data = 'No task_id in the request'
    else:
        data = 'This is not an ajax request'

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def index(request):
    if 'job' in request.GET:
        job_id = request.GET['job']
        job = AsyncResult(job_id)
        data = job.result or job.state
        print(job.result)

        context = {
            'data':data,
            'task_id':job_id,
        }
        return render(request,"show_t.html",context)
    elif 'n' in request.GET:
        print('n')
        n = request.GET['n']
        job = fft_random.delay(int(n))
        print(reverse('index'))
        return HttpResponseRedirect(reverse('index') + '?job=' + job.id)
    else:
        form = UserForm()
        context = {
            'form':form,
        }
        return render(request,"post_form.html",context)


def testTask(request):
    if 'job' in request.GET:
        job_id = request.GET['job']
        job = AsyncResult(job_id)
        data =  job.state
        print(job.state)

        context = {
            'data':data,
            'task_id':job_id,
        }
        return render(request,"test.html",context)
    elif 'a' in request.GET:
        a = request.GET['a']
        #job = taskState.delay()
        job = taskState.apply_async(args=[10],countdown=10)
        print(job.id)
        return HttpResponseRedirect('/index/' + '?job=' + job.id)

def addJob(request):
    if 'jobName' in request.GET:
        jobName = request.GET['jobName']
        #job = taskState.apply_async(args=[10], countdown=3)
        #print(job.name)
        #state = job.state
        #jobInfo = JobInfo.objects.create(jobName=jobName,jobId=job.id,status=state)
        #jobInfo.save()
        name = taskState.__name__
        print(name)
        taskScheduler = TaskScheduler.schedule_every(name, 'seconds', 20, [3])
        taskScheduler.start()

        return HttpResponseRedirect('/index/getalljobs')
    else:
        form = JobForm()
        context = {
            'form': form,
        }
        return render(request, "addJob.html", context)

def getStateByJobId(jobId):
    job = AsyncResult(jobId)
    return job.state

def getStateByJobName(jobName):
    job = AsyncResult(jobName)
    return job.state

def revokeJobByJobId(jobId):
    from celery import app
    app.control.revoke(jobId)

def startPeriodicTaskByJobId(jobId):
    from celery import schedules


def getAllJobs(request):
    jobList = JobInfo.objects.all()
    results = []
    for jobInfo in jobList:
        jobInfoJson = {}
        jobInfoJson['jobId'] = jobInfo.jobId
        jobInfoJson['jobName'] = jobInfo.jobName
        status = getStateByJobId(jobInfo.jobId)
        if(status != jobInfo.status):
            JobInfo.objects.filter(jobId=jobInfo.jobId).update(status=status)
        jobInfoJson['status'] = status
        results.append(jobInfoJson)

    jobListJson = json.dumps(results)
    print(jobListJson)
    return render(request,"showAllJobs.html",{"jobListJson": json.loads(jobListJson)})
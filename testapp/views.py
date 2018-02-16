from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import loader
from .forms import UserForm
from .tasks import *
from .testTask import add
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
    print("test task")
    if 'job' in request.GET:
        job_id = request.GET['job']
        job = AsyncResult(job_id)
        data =  job.state
        print(job.result)

        context = {
            'data':data,
            'task_id':job_id,
        }
        return render(request,"test.html",context)
    elif 'a' in request.GET:
        a = request.GET['a']
        job = taskState.delay()
        print(job.id)
        return HttpResponseRedirect('/index/' + '?job=' + job.id)
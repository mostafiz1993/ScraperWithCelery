import time
from celery import shared_task,current_task

from numpy import random
from scipy.fftpack import fft

from .TaskState import *


@shared_task
def fft_random(n):
    """
    Brainless number crunching just to have a substantial task:
    """
    for i in range(n):
        x = random.normal(0, 0.1, 2000)
        y = fft(x)
        if(i%30 == 0):
            process_percent = int(100 * float(i) / float(n))
            current_task.update_state(state='PROGRESS',
                                      meta={'process_percent': process_percent})
    return random.random()

@shared_task
def add(x,y):
    for i in range(10000):
        a = x+y
    return x+y

@shared_task
def taskState(sleepTime):
    print("sleepTime: " + str(sleepTime))
    current_task.update_state(state=TaskState.STARTING)

    time.sleep(sleepTime)
    current_task.update_state(state=TaskState.STARTED)
    i = 0
    while(True):
        i = i + 1
        time.sleep(sleepTime)
        current_task.update_state(state=TaskState.RUNNING)
        print("running" + str(i))
    time.sleep(sleepTime)
    current_task.update_state(state=TaskState.SUCCESS)
    print("finished")



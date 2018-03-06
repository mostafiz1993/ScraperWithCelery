import time
from celery import shared_task,current_task
from .TaskState import *

@shared_task
def taskState(firstTime,secondTime):
    print("sleepTime: " + str(firstTime))
    current_task.update_state(state=TaskState.SCHEDULED)

    time.sleep(firstTime)
    current_task.update_state(state=TaskState.STARTED)

    i = 0
    while(True):
        i = i + 1
        current_task.update_state(state=TaskState.RUNNING)
        print("running" + str(i))
        time.sleep(firstTime)
        current_task.update_state(state=TaskState.SUCCESS)


        if(secondTime<=0):
            break
        time.sleep(secondTime)


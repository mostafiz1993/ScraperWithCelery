from celery import shared_task,current_task

@shared_task
def add(x,y):
    for i in range(100000):
        a = x+y
    return x+y

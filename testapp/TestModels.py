from djcelery.models import PeriodicTask, IntervalSchedule
from datetime import datetime
from django.db import models

class TaskScheduler(models.Model):
    periodic_task = models.ForeignKey(PeriodicTask)

    @staticmethod
    def schedule_every(task_name, period, every, args=None, kwargs=None):
        """ schedules a task by name every "every" "period". So an example call would be:
             TaskScheduler('mycustomtask', 'seconds', 30, [1,2,3])
             that would schedule your custom task to run every 30 seconds with the arguments 1,2 and 3 passed to the actual task.
        """

        permissible_periods = ['days', 'hours', 'minutes', 'seconds']
        if period not in permissible_periods:
            raise Exception('Invalid period specified')
        # create the periodic task and the interval
        ptask_name = "%s_%s" % (task_name, datetime.now())  # create some name for the period task
        print(ptask_name + " **********************************")
        interval_schedules = IntervalSchedule.objects.filter(period=period, every=every)
        if interval_schedules:  # just check if interval schedules exist like that already and reuse em
            interval_schedule = interval_schedules[0]
        else:  # create a brand new interval schedule
            interval_schedule = IntervalSchedule()
            interval_schedule.every = every  # should check to make sure this is a positive int
            interval_schedule.period = period
            interval_schedule.save()
        ptask = PeriodicTask(name=ptask_name, task=task_name, interval=interval_schedule)
        if args:
            ptask.args = args
        if kwargs:
            ptask.kwargs = kwargs
        ptask.save()
        return TaskScheduler.objects.create(periodic_task=ptask)


    def stop(self):
        ptask = self.periodic_task
        ptask.enabled = False
        ptask.save()

    def start(self):
        ptask = self.periodic_task
        ptask.enabled = True
        ptask.save()

    def terminate(self):
        self.stop()
        ptask = self.periodic_task
        self.delete()
        ptask.delete()
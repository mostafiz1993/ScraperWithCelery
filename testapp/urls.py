from django.conf.urls import url
from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'celery_try.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^$', views.index,name='index'),
    url(r'^$', views.testTask,name='testtask'),
    url(r'^poll_state$', views.poll_state,name='poll_state'),
    url(r'^getalljobs$', views.getAllJobs,name='getAllJobs'),
    url(r'^killallrunningjobs$', views.killAllRunningJob,name='killAllRunningJobs'),
    url(r'^addjob$', views.addJob,name='addJob'),
]

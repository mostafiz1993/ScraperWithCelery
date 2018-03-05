from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^$', views.index, name = 'index'),
    url(r'index/',views.index, name = 'index'),
    url(r'addparserjob/',views.addParserJob, name = 'addparserjob'),
    url(r'addjobinscheduler',views.addJobInScheduler, name = 'addjobinscheduler'),
    url(r'deletejobparser/(?P<jobparserid>(\d+))', views.deleteJobParser, name='deletejobparser'),
    url(r'deletejobscheduler/(?P<jobschedulerid>(\d+))', views.deleteJobScheduler, name='deletejobscheduler'),
    #url(r'logout/', views.logout_view, name='logout'),
]
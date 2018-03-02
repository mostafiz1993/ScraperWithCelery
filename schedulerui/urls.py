from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name = 'home'),
    url(r'index/',views.index, name = 'index'),
    url(r'addparserjob/',views.addParserJob, name = 'addparserjob'),
    url(r'addjobinscheduler',views.addJobInScheduler, name = 'addjobinscheduler'),
    url(r'deletejobparser/(?P<jobparserid>(\d+))', views.deleteJobParser, name='deletejobparser')
]
from django.conf.urls import patterns, url
from taskq import views

urlpatterns = patterns( '',
    url(r'^add/$', views.add_task, name='add_task'),
    url(r'^edit/(?P<task_id>\w+)/$', views.edit_task, name='edit_task'),
    url(r'^delete/(?P<task_id>\w+)/$', views.delete_task, name='delete_task'),
    url(r'^list/$', views.task_list, name='task_list'),
)

from django.conf.urls import patterns, url
from taskq import views

urlpatterns = patterns( '',
    url(r'^create/$', views.create_task, name='create_task'),
    url(r'^edit/(?P<task_id>\w+)/$', views.edit_task, name='edit_task'),
    url(r'^list/$', views.list_task, name='list_task'),
)

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls import handler400, handler403
from django.conf.urls import handler404, handler500

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'fixit.views.home', name='home'),
    url(r'^$', 'taskq.views.task_list', name='task_list'),

    url(r'^admin_profile/', include('admin_profile.urls')),

    #url(r'^admin_login/$', 'fixit.views.admin_login', name='admin_login'),
    #url(r'^admin_logout/$', 'fixit.views.admin_logout', name='admin_logout'),

    url(r'^task/', include('taskq.urls')),
    url(r'^admin/', include(admin.site.urls)),
)


handler400 = "fixit.views.handle400"
handler403 = "fixit.views.handle403"
handler404 = "fixit.views.handle404"
handler500 = "fixit.views.handle500"


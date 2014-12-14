from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'fixit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin_login/$', 'fixit.views.admin_login', name='admin_login'),
    url(r'^admin_logout/$', 'fixit.views.admin_logout', name='admin_logout'),

    url(r'^task/', include('taskq.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

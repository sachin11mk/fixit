from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^admin-login/$', 'admin_profile.views.login', name="admin_login"),
    url(r'^admin-logout/$', 'admin_profile.views.logout', name='admin_logout'),
)


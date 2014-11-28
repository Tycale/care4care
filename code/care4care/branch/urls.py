from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    url(r'^new/$', 'branch.views.branch_create', name='branch_create'),
    url(r'^b/(?P<id>\d+)/(?P<slug>[-\w\d]+)/$', 'branch.views.branch_home', name='branch_home'),
    url(r'^leave/(?P<branch_id>\d+)/(?P<user_id>\d+)/$', 'branch.views.branch_leave', name='branch_leave'),
    url(r'^delete/(?P<branch_id>\d+)/$', 'branch.views.branch_delete', name='branch_delete'),
    url(r'^join/$', 'branch.views.branch_join', name='branch_join'),
    url(r'^b/(?P<branch_id>\d+)/(?P<slug>[-\w\d]+)/jobs/', include('branch.urls_job')),
)

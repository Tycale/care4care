from django.conf.urls import patterns, url, include

from branch.views import CreateSuccessDemand

urlpatterns = patterns(
    '',
    url(r'^new/$', 'branch.views.branch_create', name='branch_create'),
    url(r'^b/(?P<branch_id>\d+)/(?P<slug>[-\w\d]+)/$', 'branch.views.branch_home', name='branch_home'),
    url(r'^leave/(?P<branch_id>\d+)/(?P<user_id>\d+)/$', 'branch.views.branch_leave', name='branch_leave'),
    url(r'^ban/(?P<branch_id>\d+)/(?P<user_id>\d+)/$', 'branch.views.branch_ban', name='branch_ban'),
    url(r'^unban/(?P<branch_id>\d+)/(?P<user_id>\d+)/$', 'branch.views.branch_unban', name='branch_unban'),
    url(r'^promote/(?P<branch_id>\d+)/(?P<user_id>\d+)/$', 'branch.views.branch_promote', name='branch_promote'),
    url(r'^demote/(?P<branch_id>\d+)/(?P<user_id>\d+)/$', 'branch.views.branch_demote', name='branch_demote'),
    url(r'^delete/(?P<branch_id>\d+)/$', 'branch.views.branch_delete', name='branch_delete'),
    url(r'^join/$', 'branch.views.branch_join', name='branch_join'),

    url(r'^volunteer/(?P<volunteer_id>\d+)/accept/', 'branch.views.volunteer_accept', name='volunteer_accept'),
    url(r'^volunteer/(?P<volunteer_id>\d+)/decline/', 'branch.views.volunteer_decline', name='volunteer_decline'),

    # success form
    url(r'^volunteer/success/create/(?P<demand_id>\d+)/$',
         CreateSuccessDemand.as_view(),
         name='success_demand'),
    url(r'^volunteer/unsuccess/(?P<demand_id>\d+)/$',
         'branch.views.unsuccess_job',
         name='unsuccess_job'),
    url(r'^success/manage/(?P<success_demand_id>\d+)/$',
         'branch.views.manage_success',
         name='manage_success'),

    url(r'^b/(?P<branch_id>\d+)/(?P<slug>[-\w\d]+)/jobs/', include('branch.urls_job')),
)

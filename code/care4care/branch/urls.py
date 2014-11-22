from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'main.views.home', name='home'),
    url(r'^new/$', 'branch.views.branch_create', name='branch_create'),
    url(r'^b/(?P<id>\d+)/(?P<slug>[-\w\d]+)/$', 'branch.views.branch_home', name='branch_home')
)

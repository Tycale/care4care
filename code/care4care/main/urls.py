from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    url(r'^$', 'main.views.home', name='home'),
    url(r'^accounts/logout/$', 'main.views.logout', name='logout'),
    url(r'^accounts/login/$', 'main.views.login', name='login'),

    url(r'^accounts/', include('main.urls_register')),
    url(r'^accounts/', include('main.urls_profile')),
    url(r'^accounts/', include('main.urls_verified')),

	url(r'^statistics/$', 'main.views.statistics', name='stats'),
)

from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    url(r'^$', 'main.views.home', name='home'),
    url(r'^accounts/logout/$', 'main.views.logout', name='logout'),
    url(r'^accounts/login/$', 'main.views.login', name='login'),
    url(r'^accounts/', include('registration.backends.default.urls')),
)

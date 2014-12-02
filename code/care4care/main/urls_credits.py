from django.conf.urls import patterns, url

from main.views import credits_view

urlpatterns = patterns('',
                       url(r'^credits/menu/$',
                           credits_view,
                           name='credits'),
                       )

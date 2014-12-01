from django.conf.urls import patterns, url

from main.views import search_view

urlpatterns = patterns('',
                       url(r'^$',
                           search_view,
                           name='search'),
                       )

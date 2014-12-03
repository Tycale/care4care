from django.conf.urls import patterns, url

from main.views import search_view, job_search_view

urlpatterns = patterns('',
                       url(r'^$',
                           search_view,
                           name='search'),
                       url(r'^job/$',
                           job_search_view,
                           name='job_search'),
                       )

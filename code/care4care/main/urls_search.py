from django.conf.urls import patterns, url

from main.views import search_view, job_search_view, job_result_view

urlpatterns = patterns('',
                       url(r'^$',
                           search_view,
                           name='search'),
                       url(r'^job/$',
                           job_search_view,
                           name='job_search'),
                       url(r'^job/result/$',
                           job_result_view,
                           name='job_result'),
                       )

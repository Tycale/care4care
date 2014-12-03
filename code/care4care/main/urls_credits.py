from django.conf.urls import patterns, url

from main.views import credits_view

urlpatterns = patterns('',
                       url(r'^credit/$',
                           credits_view,
                           name='credit_page'),
                       )

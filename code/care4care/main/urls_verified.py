from django.conf.urls import patterns, url

from main.views import verified_profile_view,verified_documents_view

urlpatterns = patterns('',
                       url(r'^verified/profile/$',
                           verified_profile_view,
                           name='verified_profile'),
                       url(r'^verified/documents/$',
                           verified_documents_view,
                           name='verified_documents'),
                       )

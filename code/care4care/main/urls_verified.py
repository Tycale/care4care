from django.conf.urls import patterns, url

from main.views import VerifiedProfileView,verified_documents_view,verified_display_view,verified_status_giving_view, verified_status_refuse_view

urlpatterns = patterns('',
                       url(r'^verified/profile/(?P<user_id>\d+)/$',
                           VerifiedProfileView.as_view(),
                           name='verified_profile'),
                       url(r'^verified/documents/$',
                           verified_documents_view,
                           name='verified_documents'),
                       url(r'^verified/display/(?P<user_id>\d+)/$',
                           verified_display_view,
                           name='verified_display'),
                       url(r'^verified/status/giving/(?P<user_id>\d+)/$',
                           verified_status_giving_view,
                           name='verified_giving_status'),
                       url(r'^verified/status/refuse/(?P<user_id>\d+)/$',
                           verified_status_refuse_view,
                           name='verified_refuse_status'),
                       )

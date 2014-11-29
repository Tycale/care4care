from django.conf.urls import patterns, url

from main.views import VerifiedProfileView,verified_documents_view,verified_display_view

urlpatterns = patterns('',
                       url(r'^verified/profile/(?P<user_id>\d)+/$',
                           VerifiedProfileView.as_view(),
                           name='verified_profile'),
                       url(r'^verified/documents/$',
                           verified_documents_view,
                           name='verified_documents'),
                       url(r'^verified/display/(?P<user_id>\d+)/$',
                           verified_display_view,
                           name='verified_display'),
                       )

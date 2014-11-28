from django.conf.urls import patterns, url

from main.views import verified_member_demand_view_1,verified_member_demand_view_2

urlpatterns = patterns('',
                       url(r'^verified/profile/$',
                           verified_member_demand_view_1,
                           name='verified_member_demand_1'),
                       url(r'^verified/documents/$',
                           verified_member_demand_view_2,
                           name='verified_member_demand_2'),
                       )

from django.conf.urls import patterns, url

from main.views import verified_member_demand_view

urlpatterns = patterns('',
                       url(r'^verified/$',
                           verified_member_demand_view.as_view(),
                           name='verified_member_demand'),
                       )

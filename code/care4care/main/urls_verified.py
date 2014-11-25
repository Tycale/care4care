from django.conf.urls import patterns, url

from main.views import verified_member_demand_view, verified_member_document_view

urlpatterns = patterns('',
                       url(r'^verified/$',
                           verified_member_demand_view,
                           name='verified_member_demand'),
                       url(r'^verified/documents/(?P<recomendation_letter_1>\w+).pdf/$',
                       		verified_member_document_view,
                       		name='verified_member_r1'),
                       url(r'^verified/documents/(?P<recomendation_letter_2>\w+).pdf/$',
                       		verified_member_document_view,
                       		name='verified_member_r2'),
                       url(r'^verified/documents/(?P<criminal_record>\w+).pdf/$',
                       		verified_member_document_view,
                       		name='verified_member_cr')
                       )

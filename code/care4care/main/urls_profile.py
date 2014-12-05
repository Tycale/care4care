from django.conf.urls import patterns, url

from django.views.generic.base import TemplateView

from main.views import user_profile, manage_profile, EditProfileView, member_favorite, \
                        member_personal_network, AddEmergencyContact, EmergencyContactDetails, \
                        UpdateEmergencyContact,member_ignore_list, EditNonProfileView

urlpatterns = patterns('',
                       url(r'^profile/$',
                           manage_profile,
                           name='profile'),
                       url(r'^profile/edit/(?P<user_id>\d+)/$',
                           EditProfileView.as_view(),
                           name='edit_profile'),
                       url(r'^profile/edit/pro/(?P<user_id>\d+)/$',
                           EditNonProfileView.as_view(),
                           name='edit_non_profile'),
                       url(r'^profile/(?P<user_id>\d+)/$',
                           user_profile,
                           name='user_profile'),
                       url(r'^profile/add_emergency_contact/(?P<user_id>\d+)/',
                           AddEmergencyContact.as_view(),
                           name='add_emergency_contact'),
                       url(r'^profile/see_emergency_contact/(?P<emergency_id>\d+)/',
                           EmergencyContactDetails.as_view(),
                           name='see_emergency_contact'),
                       url(r'^profile/(?P<user_id>\d+)/update_emergency_contact/(?P<emergency_id>\d+)/',
                           UpdateEmergencyContact.as_view(),
                           name='update_emergency_contact'),
                       url(r'^profile/network/$',
                           TemplateView.as_view(template_name='profile/personal_network.html'),
                           name='personal_network'),
                       url(r'^api/member_favorite/(?P<user_id>\d+)/$',
                           member_favorite,
                           name='member_favorite'),
                       url(r'^api/member_personal_network/(?P<user_id>\d+)/$',
                          member_personal_network,
                          name='member_personal_network'),
                       url(r'^api/ignore_list/(?P<user_id>\d+)/$',
                             member_ignore_list,
                             name='member_ignore_list'),
                       )

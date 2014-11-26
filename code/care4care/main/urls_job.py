from django.conf.urls import patterns, url

from django.views.generic.base import TemplateView

from main.views import NeedHelpView

from main.forms import NeedHelpForm

from main.views import user_profile, manage_profile, EditProfileView, member_favorite, member_personal_network

urlpatterns = patterns('',
                       url(r'^$',
                           manage_profile,
                           name='profile_management'),
                       url(r'^needhelp/$',
                           NeedHelpView.as_view(),
                           name='need_help'),
                       url(r'^offerhelp/$',
                            NeedHelpView.as_view(),
                           name='offer_help'),
                       )

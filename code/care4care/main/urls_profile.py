from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.views.generic.base import TemplateView

from registration.backends.default.views import ActivationView
#from registration.backends.default.views import RegistrationView

from main.views import RegistrationView
from main.views import user_profile, manage_profile, edit_profile

urlpatterns = patterns('',
                       url(r'^profile/$',
                           manage_profile,
                           name='profile_management'),
                       url(r'^profile/edit/$',
                           edit_profile.as_view(),
                           name='edit_profile'),
                       url(r'^profile/(?P<user_id>)/$',
                           user_profile,
                           name='user_profile'),
                       url(r'^profile/network/$',
                           TemplateView.as_view(template_name='profile/personal_network.html'),
                           name='personal_network')
                       )

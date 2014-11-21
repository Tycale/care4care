from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.views.generic.base import TemplateView

from registration.backends.default.views import ActivationView

from main.views import RegistrationView

from main.forms import CareRegistrationForm

urlpatterns = patterns('',
                       url(r'^verified/$',
                           TemplateView.as_view(template_name='verified/verified_member_demand.html'),
                           name='verified_member_demand'),
                       )

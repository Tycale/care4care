from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

from registration.backends.default.views import ActivationView

from main.views import RegistrationView

from main.forms import CareRegistrationForm

from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
                       url(r'^activate/complete/$',
                           TemplateView.as_view(template_name='registration/activation_complete.html'),
                           name='registration_activation_complete'),
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       url(r'^activate/(?P<activation_key>\w+)/$',
                           ActivationView.as_view(),
                           name='registration_activate'),
                       url(r'^register/$',
                           RegistrationView.as_view(form_class=CareRegistrationForm),
                           name='registration_register'),
                       url(r'^register/complete/$',
                           TemplateView.as_view(template_name='registration/registration_complete.html'),
                           name='registration_complete'),
                       url(r'^password/change/$',
                           auth_views.password_change,
                           {'template_name' : 'registration/password_change.html'},
                           name='auth_password_change'),
                       url(r'^password/change/done/$',
                           auth_views.password_change_done,
                           name='password_change_done'),
                       url(r'^password/reset/$',
                           auth_views.password_reset,
                           {'template_name' : 'registration/password_reset.html',
                            'email_template_name' : 'registration/pass_reset_email.html',
                            'subject_template_name' : 'registration/pass_reset_subject.txt',},
                           name='password_reset'),
                       url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                           auth_views.password_reset_confirm,
                           {'template_name' : 'registration/pass_reset_form.html'},
                           name='password_reset_confirm'),
                       url(r'^password/reset/complete/$',
                           auth_views.password_reset_complete,
                           {'template_name' : 'registration/pass_reset_done.html'},
                           name='password_reset_complete'),
                       url(r'^password/reset/done/$',
                           auth_views.password_reset_done,
                           {'template_name' : 'registration/pass_reset_complete.html',},
                           name='password_reset_done'),
                       )

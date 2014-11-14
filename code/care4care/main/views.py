from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout as _logout
from django.contrib.auth import authenticate, login as _login
from registration import signals

from registration.views.backends.default.views import RegistrationView as BaseRegistrationView
from main.forms import CareRegistrationForm
from main.models import User
from django.conf import settings

def home(request):
    return render(request, 'main/home.html', locals())

def logout(request):
    _logout(request)
    messages.add_message(request, messages.INFO, _('Vous êtes désormais déconnecté.'))
    return redirect('home')

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            _login(request, user)
            messages.add_message(request, messages.INFO, _('Vous êtes désormais connecté.'))
        else:
            messages.add_message(request, messages.ERROR, _('Impossible de vous connecter, vous \
                êtes innactif. Vérifiez vos emails afin de valider votre compte.'))
    else:
        messages.add_message(request, messages.ERROR, _('Impossible de se connecter.'))

    return redirect('home')

class RegistrationView(BaseRegistrationView):
    """
    A registration backend for our CareRegistrationForm
    """

    def register(self, request, **cleaned_data):
        email, password = cleaned_data['email'], cleaned_data['password1']
        first_name, last_name = cleaned_data['first_name'], cleaned_data['last_name']

        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        new_user = User.objects.create_user(email, first_name, last_name, password=password)
        new_user.birth_date = cleaned_data['birth_date']
        new_user.how_found = cleaned_data['how_found']
        new_user.languages = cleaned_data['languages']
        new_user.phone_number = cleaned_data['phone_number']
        new_user.mobile_number = cleaned_data['mobile_number']
        new_user.address = cleaned_data['address']
        new_user.city = cleaned_data['city']
        new_user.postal_code = cleaned_data['postal_code']
        new_user.contry = cleaned_data['contry']
        new_user.save()

        #new_user = authenticate(username=email, password=password)
        #_login(request, new_user)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def get_success_url(self, request, user):
        return ('registration_complete', (), {})



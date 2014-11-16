from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout as _logout
from django.contrib.auth import authenticate, login as _login
from registration import signals
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from registration.models import RegistrationProfile
from registration.backends.default.views import RegistrationView as BaseRegistrationView
from main.forms import ProfileManagementForm
from main.models import User

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

""" Get profile from a user"""
def user_profile(request, user_id):
    user_to_display = get_object_or_404(User, pk=user_id)
    return render(request, 'profile/user_profile.html',locals())

""" Return the profile from the current logged user"""
def manage_profile(request):
    user_to_display = get_object_or_404(User, pk=request.user.id)
    return render(request, 'profile/user_profile.html',locals())

""" Return the profile from the current logged user"""
def edit_profile(request):
    form = ProfileManagementForm(instance=request.user)
    return render(request,'registration/registration_form.html',locals())

class RegistrationView(BaseRegistrationView):
    """
    A registration backend for our CareRegistrationForm
    """

    def register(self, request, **cleaned_data):
        username, email, password = cleaned_data['username'], cleaned_data['email'], cleaned_data['password1']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        first_name = cleaned_data['first_name']
        last_name = cleaned_data['last_name']
        username = '{} {}'.format(first_name, last_name)
        new_user = RegistrationProfile.objects.create_inactive_user(
            username, email, password, site,
            send_email=self.SEND_ACTIVATION_EMAIL,
            request=request,
        )
        new_user.last_name = last_name
        new_user.first_name = first_name
        new_user.birth_date = cleaned_data['birth_date']
        new_user.how_found = cleaned_data['how_found']
        new_user.languages = cleaned_data['languages']
        new_user.phone_number = cleaned_data['phone_number']
        new_user.mobile_number = cleaned_data['mobile_number']
        new_user.address = cleaned_data['address']
        new_user.city = cleaned_data['city']
        new_user.postal_code = cleaned_data['postal_code']
        new_user.country = cleaned_data['country']
        new_user.save()

        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

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
from django.views.generic import View
from main.forms import ProfileManagementForm
from main.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect

def home(request):
    return render(request, 'main/home.html', locals())

def logout(request):
    _logout(request)
    messages.add_message(request, messages.INFO, _('Vous êtes désormais déconnecté.'))
    return redirect('home')

def login(request):
    redirect_to = request.POST.get('next',
                                   request.GET.get('next', '/'))

    if request.POST and 'username' in request.POST and 'password' in request.POST :
        username = request.POST['username'].lower()
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                _login(request, user)
                messages.add_message(request, messages.INFO, _('Vous êtes désormais connecté.'))
                return HttpResponseRedirect(redirect_to)
            else:
                messages.add_message(request, messages.ERROR, _('Impossible de vous connecter, vous \
                    êtes innactif. Vérifiez vos emails afin de valider votre compte.'))
        else:
            messages.add_message(request, messages.ERROR, _('Impossible de se connecter.'))
    return render(request, 'profile/login.html',locals())


def user_profile(request, user_id):
    """ Get profile from a user"""
    user_to_display = get_object_or_404(User, pk=user_id)
    return render(request, 'profile/user_profile.html',locals())


@login_required
def manage_profile(request):
    """ Return the profile from the current logged user"""
    user_to_display = get_object_or_404(User, pk=request.user.id)
    return render(request, 'profile/user_profile.html',locals())


class EditProfileView(View):
    """ Return the edit page for the current logged user"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditProfileView, self).dispatch(*args, **kwargs)

    def get(self, request):
        user = request.user
        form = ProfileManagementForm(instance=user)
        return render(request,'profile/edit_profile.html',locals())

    def post(self, request):
        user = request.user
        form = ProfileManagementForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, _('Modification sauvegardée'))
        else:
            form = ProfileManagementForm(instance=request.user)
        return render(request,'profile/edit_profile.html',locals())


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
        new_user.longitude = cleaned_data['longitude']
        new_user.latitude = cleaned_data['latitude']
        new_user.location = cleaned_data['location']
        new_user.save()

        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

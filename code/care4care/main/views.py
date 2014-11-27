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
from main.forms import ProfileManagementForm, VerifiedInformationForm, EmergencyContactCreateForm
from main.models import User, VerifiedInformation, EmergencyContact
from branch.models import Job
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from branch.models import Branch, BranchMembers

import json
import os
from os.path import abspath, dirname

from django.utils import timezone
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin

def home(request):
    user = request.user
    demands = Job.objects.filter(donor=None)
    offers = Job.objects.filter(receiver=None)
    if user.is_authenticated() :
        demands.filter(branch__in=user.membership.all())
        offers.filter(branch__in=user.membership.all())
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
                    êtes inactif. Vérifiez vos emails afin de valider votre compte.'))
        else:
            messages.add_message(request, messages.ERROR, _('Impossible de se connecter.'))
    return render(request, 'profile/login.html',locals())


def user_profile(request, user_id):
    """ Get profile from a user"""
    id_int = int(user_id)
    user_to_display = get_object_or_404(User, pk=id_int)
    user = get_object_or_404(User, pk=request.user.id)
    is_my_friend = False
    if (user_to_display in user.favorites.all()):
        is_my_friend = True
    return render(request, 'profile/user_profile.html',locals())


@login_required
def manage_profile(request):
    """ Return the profile from the current logged user"""
    user_to_display = get_object_or_404(User, pk=request.user.id)
    user_to_display = User.objects.select_related().get(id=request.user.id)

    return render(request, 'profile/user_profile.html',locals())


@user_passes_test(lambda u: not u.is_verified)
@login_required
def verified_member_demand_view(request):
    user = request.user
    form = VerifiedInformationForm()

    try:
        old_vi = VerifiedInformation.objects.get(user=user)
        form = VerifiedInformationForm(instance=old_vi)
    except VerifiedInformation.DoesNotExist:
        pass

    if request.POST :
        form = VerifiedInformationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                old_vi.delete()
            except UnboundLocalError:
                pass
            obj = form.save(commit=False)
            obj.user = user
            obj.save()
            messages.add_message(request, messages.INFO, _('Modification sauvegardée'))
            return redirect('home')

    return render(request,'verified/verified_member_demand.html',locals())

def statistics(request):
    return render(request, 'statistics/statistics.html', locals())


@login_required
def member_favorite(request, user_id):
    user = get_object_or_404(User, pk=request.user.id)
    id_favorite = user_id
    favorite_user = get_object_or_404(User, pk=id_favorite)
    if request.method == "PUT":
        user.favorites.add(favorite_user)
        user.save()
        return HttpResponse(
            json.dumps({"name": favorite_user.get_full_name()}),
            content_type="application/json"
        )

    elif request.method == 'DELETE':
        user.favorites.remove(favorite_user)
        user.save()
        return HttpResponse(json.dumps({"name": favorite_user.get_full_name()}), content_type='application/json')

@login_required
def member_personal_network(request, user_id):
    user = get_object_or_404(User, pk=request.user.id)
    id_other = user_id
    other_user = get_object_or_404(User, pk=id_other)
    if request.method == "PUT":
        user.personal_network.add(other_user)
        user.save()
        return HttpResponse(
            json.dumps({"name": other_user.get_full_name()}),
            content_type="application/json"
        )

    elif request.method == 'DELETE':
        user.personal_network.remove(other_user)
        user.save()
        return HttpResponse(json.dumps({"name": other_user.get_full_name()}), content_type='application/json')


# Classes views

class EditProfileView(UpdateView, SuccessMessageMixin):
    """ Return the edit page for the current logged user"""
    form_class = ProfileManagementForm
    model = User
    template_name = 'profile/edit_profile.html'
    success_message = _('Profil modifié avec succès !')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditProfileView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('profile')


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
        #new_user.languages = cleaned_data['languages']
        new_user.phone_number = cleaned_data['phone_number']
        new_user.mobile_number = cleaned_data['mobile_number']
        #new_user.longitude = cleaned_data['longitude']
        #new_user.latitude = cleaned_data['latitude']
        #new_user.location = cleaned_data['location']

        
        new_user.save()
        branch = Branch.objects.get(pk=cleaned_data['id'])
        bm = BranchMembers(user=new_user, branch=branch, is_admin=False, joined=timezone.now())
        bm.save()

        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        context['branches'] = Branch.objects.all()
        return context

class EmergencyContact(CreateView):
    template_name = 'profile/emergency_contact.html'
    form_class = EmergencyContactCreateForm
    model = EmergencyContact

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EmergencyContact, self).form_valid(form)

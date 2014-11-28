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
from main.forms import ProfileManagementForm, VerifiedInformationForm, EmergencyContactCreateForm
from main.models import User, VerifiedInformation, EmergencyContact
from branch.models import Job
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from branch.models import Branch, BranchMembers

from django.views.generic.detail import DetailView

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
    user_to_display = get_object_or_404(User, pk=user_id)
    user = request.user
    is_my_friend = False
    is_in_my_network = False
    if user_to_display in user.favorites.all():
        is_my_friend = True
    if user_to_display in user.personal_network.all():
        is_in_my_network = True
    if user_to_display.id == user_id:
        pending_offers = Job.objects.filter(donor=user_to_display )
    return render(request, 'profile/user_profile.html',locals())


@login_required
def manage_profile(request):
    """ Return the profile from the current logged user"""
    user_to_display = request.user

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
    user = request.user
    favorite_user = get_object_or_404(User, pk=user_id)
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
    user = request.user
    id_other = user_id
    other_user = get_object_or_404(User, pk=user_id)
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
        obj = self.get_object()
        if obj.id != self.request.user.id and not self.request.user.is_superuser :
            return redirect(obj.get_absolute_url())
        return super(EditProfileView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.kwargs['user_id'])

    def get_success_url(self):
        return self.get_object().get_absolute_url()


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

class AddEmergencyContact(CreateView):
    template_name = 'profile/emergency_contact.html'
    form_class = EmergencyContactCreateForm
    model = EmergencyContact

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        if obj.id != self.request.user.id and not self.request.user.is_superuser :
            return redirect(obj.get_absolute_url())
        return super(AddEmergencyContact, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.kwargs['user_id'])

    def form_valid(self, form):
        form.instance.user = User.objects.get(pk=self.kwargs['user_id'])
        return super(AddEmergencyContact, self).form_valid(form)

    def get_success_url(self):
        return self.get_object().get_absolute_url()

class EmergencyContactDetails(DetailView):
    model = EmergencyContact
    template_name = 'profile/emergency_details.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        # TODO: check verified_work_with
        if obj.id != self.request.user.id and not self.request.user.is_superuser and self.request.user not in obj.verified_work_with.all():
            return redirect(obj.get_absolute_url())
        return super(EmergencyContactDetails, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EmergencyContactDetails, self).get_context_data(**kwargs)
        return context

    def get_object(self):
        return EmergencyContact.objects.get(pk=self.kwargs['emergency_id'])

class UpdateEmergencyContact(UpdateView):
    template_name = 'profile/modify_emergency.html'
    form_class = EmergencyContactCreateForm
    model = EmergencyContact

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        if obj.id != self.request.user.id and not self.request.user.is_superuser :
            return redirect(obj.get_absolute_url())
        return super(UpdateEmergencyContact, self).dispatch(*args, **kwargs)

    def get_object(self):
        return EmergencyContact.objects.get(pk=self.kwargs['emergency_id'])

    def form_valid(self, form):
        form.instance.user = User.objects.get(pk=self.kwargs['user_id'])
        return super(UpdateEmergencyContact, self).form_valid(form)

    def get_success_url(self):
        return User.objects.get(pk=self.kwargs['user_id']).get_absolute_url()



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
from main.forms import ProfileManagementForm, VerifiedInformationForm, EmergencyContactCreateForm, VerifiedProfileForm
from main.models import User, VerifiedInformation, EmergencyContact, Statistics
from branch.models import Demand, Offer
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from branch.models import Branch, BranchMembers
from postman.api import pm_write

from django.views.generic.detail import DetailView

from main.models import Color
import json
import sys
from os.path import abspath, dirname
import datetime

from django.utils import timezone
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin

def home(request):
    user = request.user

    not_enough = True
    if user.is_authenticated():
        branch_ids = [b.branch.id for b in user.membership.all()]
        demands = Demand.objects.filter(branch__in=branch_ids).all()
        offers = Offer.objects.filter(branch__in=branch_ids).all()
        if demands.count() > 3 or offers.count() > 3:
            not_enough = False

    if not_enough:
        demands = Demand.objects.all()
        offers = Offer.objects.all()

    return render(request, 'main/home.html', locals())

def logout(request):
    _logout(request)
    messages.add_message(request, messages.INFO, _('Vous êtes désormais déconnecté.'))
    return redirect('home')

def login(request):
    redirect_to = request.POST.get('next',
                                   request.GET.get('next', '/'))

    if request.POST and 'username' in request.POST and 'password' in request.POST:
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
    return render(request, 'profile/login.html', locals())


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
    return render(request, 'profile/user_profile.html', locals())


@login_required
def manage_profile(request):
    """ Return the profile from the current logged user"""
    user_to_display = request.user
    pending_offers = Offer.objects.filter(donor=user_to_display)
    return render(request, 'profile/user_profile.html', locals())

"""@user_passes_test(lambda u: not u.is_verified)
@login_required
def verified_profile_view(request):
    user = request.user
    form = VerifiedProfileForm(instance=user)
    if request.POST :
        form = VerifiedProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, _('Modification sauvegardée'))
            return redirect('verified_documents')
    return render(request,'verified/verified_profile.html', locals())"""


# Classes views
class VerifiedProfileView(UpdateView, SuccessMessageMixin):
    """ Return the edit page for the current logged user"""
    form_class = VerifiedProfileForm
    model = User
    template_name = 'verified/verified_profile.html'
    success_message = _('Profil modifié avec succès !')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        if obj.id != self.request.user.id and not self.request.user.is_superuser:
            return redirect(obj.get_absolute_url())
        return super(VerifiedProfileView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.kwargs['user_id'])

    def get_success_url(self):
        return reverse('verified_documents')


@user_passes_test(lambda u: not u.is_verified)
@login_required
def verified_documents_view(request):
    user = request.user
    form = VerifiedInformationForm()
    try:
        old_vi = VerifiedInformation.objects.get(user=user)
        form = VerifiedInformationForm(instance=old_vi)
    except VerifiedInformation.DoesNotExist:
        pass

    if request.POST:
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

    return render(request,'verified/verified_documents.html', locals())

@login_required
def verified_display_view(request, user_id):
    user_to_display = get_object_or_404(User, pk=user_id)
    verified_documents = get_object_or_404(VerifiedInformation, user=user_id)
    return render(request, 'verified/verified_display.html', locals())


def verified_status_giving_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_verified = True
    user.save()
    verified_documents = get_object_or_404(VerifiedInformation, user=user_id)
    verified_documents.delete()
    subject = _("Accord du status de membre vérifié")
    body = _("Le status de membre vérifié vous a été accordé ! Félicitations.")
    pm_write(request.user, user, subject, body)
    messages.add_message(request, messages.INFO, _('Droit accordé'))
    return redirect('home')


@login_required
def verified_status_refuse_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_verified = False
    user.save()
    verified_documents = get_object_or_404(VerifiedInformation, user=user_id)
    verified_documents.delete()
    subject = _("Accord du status de membre vérifié")
    body = _("Le status de membre vérifié vous a été refusé. Pour plus d'informations, contactez l'officier responsable de votre branche.")
    pm_write(request.user, user, subject, body)
    messages.add_message(request, messages.INFO, _('Droit refusé et demande supprimée'))
    return redirect('home')


@login_required
def member_favorite(request, user_id):
    user = request.user
    favorite_user = get_object_or_404(User, pk=user_id)
    if request.method == "PUT":
        if favorite_user in user.ignore_list.all():
            return HttpResponse(json.dumps({"name": favorite_user.get_full_name()}), status=422)
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

@login_required
def member_ignore_list(request, user_id):
    user = request.user
    id_other = user_id
    other_user = get_object_or_404(User, pk=user_id)
    if request.method == "PUT":
        user.ignore_list.add(other_user)
        user.personal_network.remove(other_user)
        user.favorites.remove(other_user)
        try:
          user.save()
        except:
          e = sys.exc_info()[0]
        return HttpResponse(
            json.dumps({"name": other_user.get_full_name()}),
            content_type="application/json"
        )

    elif request.method == 'DELETE':
        user.ignore_list.remove(other_user)
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
        if obj.id != self.request.user.id and not self.request.user.is_superuser:
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

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        context['branches'] = Branch.objects.all()
        return context

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
        if obj.id != self.request.user.id and not self.request.user.is_superuser:
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
        if obj.id != self.request.user.id and not self.request.user.is_superuser:
            return redirect(obj.get_absolute_url())
        return super(UpdateEmergencyContact, self).dispatch(*args, **kwargs)

    def get_object(self):
        return EmergencyContact.objects.get(pk=self.kwargs['emergency_id'])

    def form_valid(self, form):
        form.instance.user = User.objects.get(pk=self.kwargs['user_id'])
        return super(UpdateEmergencyContact, self).form_valid(form)

    def get_success_url(self):
        return User.objects.get(pk=self.kwargs['user_id']).get_absolute_url()


@login_required
def similar_jobs(request):
    return render(request, 'seek_similar_jobs/main.html')

@login_required
def similar_demands(request):
    user = request.user
    now = datetime.datetime.now()
    user_offers = Job.objects.filter(donor = user, receiver__isnull = True, date__gte=now)

    return render(request, 'seek_similar_jobs/main.html', locals())

@login_required
def similar_offers(request):
    user = request.user
    now = datetime.datetime.now()
    user_demands = Job.objects.filter(donor__isnull = True, receiver = user, date__gte=now)
    offers = Job.objects.filter(receiver__isnull = True, date__gte=now)
    result = []
    for demand in user_demands:
        result.extend(offers.filter(branch=demand.branch, date=demand.date, category=demand.category))

    return render(request, 'seek_similar_jobs/main.html', locals())

### Statistics ###

def statistics(request):
    LIGHT_BLUE_RGB = Color.rgba(Color.LIGHT_BLUE_RGB, 1)
    GREEN_RGB = Color.rgba(Color.GREEN_RGB, 1)
    ORANGE_RGB = Color.rgba(Color.ORANGE_RGB, 1)
    return render(request, 'statistics/statistics.html', locals())

# Return json-type HttpResponse from method() result
def get_json_from(method):
    return HttpResponse(method, content_type="application/json")


def get_registrated_users_json(request):
    return get_json_from(Statistics.get_users_registrated_json())

def get_account_types_json(request):
    return get_json_from(Statistics.get_account_types_json())

def get_users_status_json(request):
    return get_json_from(Statistics.get_users_status_json())

def get_job_categories_json(request):
    return get_json_from(Statistics.get_job_categories_json())

def get_user_job_categories_json(request, user_id):
    return get_json_from(Statistics.get_user_job_categories_json(user_id))

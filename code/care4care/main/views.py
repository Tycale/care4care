from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as __
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout as _logout
from django.contrib.auth import authenticate, login as _login
from registration import signals
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from registration.models import RegistrationProfile
from registration.backends.default.views import RegistrationView as BaseRegistrationView
from main.forms import ProfileManagementForm, VerifiedInformationForm, EmergencyContactCreateForm, \
            VerifiedProfileForm, JobSearchForm, GiftForm, AddUser, NonProfileManagementForm
from main.models import User, VerifiedInformation, EmergencyContact, JobCategory, JobType, MemberType, GIVINGTO
from branch.models import Demand, Offer
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from branch.models import Branch, BranchMembers, TIME_CHOICES
from postman.api import pm_write
from django.db.models import Q
from django.views.generic.detail import DetailView
from django.core import serializers


from main.ajax.views import *
import sys
from os.path import abspath, dirname
import datetime

from django.utils import timezone
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from main.utils import can_manage, is_branch_admin, refuse, can_manage_branch_specific, is_in_branch, \
                        discriminate_demands, discriminate_offers

def home(request):
    """
        View used for the home_page.
        If the user is authenticate, show the offers and demands in his branch 
        ,he can choose if he want to see closed demands and offers.
        Otherwise he can see all offers and demands but he can't see detail.
    """
    user = request.user

    if user.is_authenticated():
        branch_ids = [b.branch.id for b in user.membership.all()]
        demands = Demand.objects.filter(branch__in=branch_ids).all()
        offers = Offer.objects.filter(branch__in=branch_ids).all()
    else :
        demands = Demand.objects.filter(receive_help_from_who=MemberType.ALL).all()
        offers = Offer.objects.filter(receive_help_from_who=MemberType.ALL).all()

    demands = demands.up_to_date()
    offers = offers.up_to_date()

    if user.is_authenticated():
        demands = discriminate_demands(request, demands)
        offers = discriminate_offers(request, offers)

    nb_branch = Branch.objects.all().count()
    branches = Branch.objects.all()
    nb_users = User.objects.all().count()

    return render(request, 'main/home.html', locals())

def help(request):
    """
        help view calling the help template           
    """

    return render(request, 'main/help.html', locals())

def jobs_care4care(request):
    """
        jobs_care4care view calling the jobs_care4care template           
    """

    return render(request, 'main/jobs_care4care.html', locals())

def about_us(request):
    """
        about_us view calling the about_us template           
    """

    return render(request, 'main/about_us.html', locals())

def what_is(request):
    """
        what_is view calling the what_is template           
    """

    return render(request, 'main/what_is.html', locals())

def logout(request):
    """
        log out the user and return to the home page
    """
    _logout(request)
    messages.add_message(request, messages.INFO, _('Vous êtes désormais déconnecté.'))
    return redirect('home')

def login(request):
    """
        log in function used and return to the home page if it success or log in page if it fail.
    """
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

@login_required
def user_profile(request, user_id):
    """ Get profile from a user"""
    user_to_display = get_object_or_404(User, pk=user_id)
    user = request.user
    in_other_network = False
    in_other_ignore_list = False
    can_manage_user = False

    if user.is_authenticated():

        if request.user.id != user_to_display.id:
            if request.user in user_to_display.personal_network.all():
                in_other_network = True
            if request.user in user_to_display.ignore_list.all():
                in_other_ignore_list = True
            if can_manage(user_to_display,user):
                can_manage_user = True
        else:
            can_manage_user = True

        if in_other_ignore_list:
            messages.add_message(request, messages.INFO, _('Vous êtes pas autoriser à consulter ce profil'))
            return redirect('home')

        pending_demands = Demand.objects.filter(donor=user_to_display)
        is_my_friend = False
        is_in_my_network = False
        if user_to_display in user.favorites.all():
            is_my_friend = True
        if user_to_display in user.personal_network.all():
            is_in_my_network = True

        form_favorite = AddUser()
        form_network = AddUser()
        form_ignored = AddUser()

        if request.POST:
            if 'favorite' in request.POST:
                form_favorite = AddUser(request.POST)
                if form_favorite.is_valid():
                    try:
                        added_user = User.objects.get(username=form_favorite.cleaned_data['user'])
                        user_to_display.favorites.add(added_user)
                        messages.add_message(request, messages.INFO, __('Utilisateur {user} ajouté').format(user=added_user))
                    except:
                        pass
                    form_favorite = AddUser()

            if 'network' in request.POST:
                form_network = AddUser(request.POST)
                if form_network.is_valid():
                    try:
                        added_user = User.objects.get(username=form_network.cleaned_data['user'])
                        user_to_display.personal_network.add(added_user)
                        messages.add_message(request, messages.INFO, __('Utilisateur {user} ajouté').format(user=added_user))
                    except:
                        pass
                    form_network = AddUser()

            if 'ignored' in request.POST:
                form_ignored = AddUser(request.POST)
                if form_ignored.is_valid():
                    try:
                        added_user = User.objects.get(username=form_ignored.cleaned_data['user'])
                        user_to_display.ignore_list.add(added_user)
                        messages.add_message(request, messages.INFO, __('Utilisateur {user} ajouté').format(user=added_user))
                    except:
                        pass
                    form_ignored = AddUser()

    return render(request, 'profile/user_profile.html', locals())


@login_required
def manage_profile(request):
    """ Return the profile from the current logged user"""
    return user_profile(request, request.user.id)


# Classes views
class VerifiedProfileView(UpdateView, SuccessMessageMixin):
    """ Return the edit page for the current logged user and ask to complete"""
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
    """ Ask 2recommendations letter and criminal record to logged user"""
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
    """show verified informations on user selected"""
    user_to_display = get_object_or_404(User, pk=user_id)
    verified_documents = get_object_or_404(VerifiedInformation, user=user_id)
    if not can_manage(user_to_display, request.user) or user_to_display.id == request.user.id:
        return refuse(request)
    return render(request, 'verified/verified_display.html', locals())


@login_required
def verified_status_giving_view(request, user_id):
    """Give verified status to user with user_id and send a message"""
    user = get_object_or_404(User, pk=user_id)
    if not can_manage(user, request.user) or user.id == request.user.id:
        return refuse(request)
    user.is_verified = True
    user.user_type = MemberType.VERIFIED_MEMBER
    user.save()
    verified_documents = get_object_or_404(VerifiedInformation, user=user_id)
    verified_documents.delete()
    subject = _("Accord du status de membre vérifié")
    body = _("Le status de membre vérifié vous a été accordé ! Félicitations.")
    pm_write(request.user, user, subject, body)
    messages.add_message(request, messages.INFO, _('Droit accordé'))
    return redirect(user.get_absolute_url())


@login_required
def verified_status_refuse_view(request, user_id):
    """Refuse verified status to user with user_id, send a specific message and remove verified demand"""
    user = get_object_or_404(User, pk=user_id)
    if not can_manage(user, request.user) or user.id == request.user.id:
        return refuse(request)
    user.is_verified = False
    user.save()
    verified_documents = get_object_or_404(VerifiedInformation, user=user_id)
    verified_documents.delete()
    subject = _("Accord du status de membre vérifié")
    body = _("Le status de membre vérifié vous a été refusé. Pour plus d'informations, contactez l'officier responsable de votre branche.")
    pm_write(request.user, user, subject, body)
    messages.add_message(request, messages.INFO, _('Droit refusé et demande supprimée'))
    return redirect(user.get_absolute_url())


@login_required
def member_favorite(request, user_id):
    "show user's favorite group where user have the id specified"
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
    "show user's personal_network where user have the id specified"
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
    "show user's ignored list where user have the id specified"
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

class EditNonProfileView(UpdateView, SuccessMessageMixin):
    """ Return the edit page for the current logged user"""
    form_class = NonProfileManagementForm
    model = User
    template_name = 'profile/edit_nonprofile.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        if obj.id != self.request.user.id and not self.request.user.is_superuser:
            return redirect(obj.get_absolute_url())
        return super(EditNonProfileView, self).dispatch(*args, **kwargs)

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
        new_user.user_type = cleaned_data['user_type']
        #new_user.languages = cleaned_data['languages']
        new_user.phone_number = cleaned_data['phone_number']
        new_user.mobile_number = cleaned_data['mobile_number']
        #new_user.longitude = cleaned_data['longitude']
        #new_user.latitude = cleaned_data['latitude']
        #new_user.location = cleaned_data['location']


        new_user.save()

        # chercher une branche uniquement pour le membre de type membre
        if int(new_user.user_type) == int(MemberType.MEMBER):
            branch = Branch.objects.get(pk=cleaned_data['id'])
            bm = BranchMembers(user=new_user, branch=branch, is_admin=False, joined=timezone.now())
            bm.save()

        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

class AddEmergencyContact(CreateView):
    """A view for add an emergency_contact"""
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
    """show the emergency_contact detail for user logged"""
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
    """A view for update an emergency_contact"""
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
    """view for matching job"""
    return render(request, 'seek_similar_jobs/main.html')

@login_required
def similar_demands(request):
    """view for matching demands"""
    user = request.user
    now = datetime.datetime.now()
    user_offers = Offer.objects.filter(donor = user, date__gte=now)
    demands = Demand.objects.filter(date__gte=now).exclude(receiver=user)
    result_demands = []
    for offer in user_offers:
        result_demands.extend(demands.filter(branch=offer.branch, date=offer.date, category=offer.category))

    return render(request, 'seek_similar_jobs/main.html', locals())

@login_required
def similar_offers(request):
    """view for matching offers"""
    user = request.user
    now = datetime.datetime.now()
    user_demands = Demand.objects.filter(receiver = user, date__gte=now)
    offers = Offer.objects.filter(date__gte=now).exclude(donor=user)
    result_offers = []
    for demand in user_demands:
        result_offers.extend(offers.filter(branch=demand.branch, date=demand.date, category=demand.category))

    return render(request, 'seek_similar_jobs/main.html', locals())

### Statistics ###

def statistics(request):
    """Stats"""
    if not request.user.is_superuser:
        return HttpResponse(PERMISSION_DENIED, status=401)

    # Account status color
    ACTIVE_COLOR = ACTIVE_COLOR_HEX
    ON_HOLIDAY_COLOR = ON_HOLIDAY_COLOR_HEX
    UNSUBSCRIBED_COLOR = UNSUBSCRIBED_COLOR_HEX

    # Account types colors
    MEMBER_COLOR = MEMBER_COLOR_HEX
    VERIFIED_MEMBER_COLOR = VERIFIED_MEMBER_COLOR_HEX
    NON_MEMBER_COLOR = NON_MEMBER_COLOR_HEX

    return render(request, 'statistics/statistics.html', locals())

# Return json-type HttpResponse from method() result
def get_json_from(text):
    return HttpResponse(text, content_type="application/json")

PERMISSION_DENIED = "Permission denied. This event will be reported."


# Global statistics

@login_required
def get_registrated_users_json_view(request):
    if not request.user.is_superuser:
        return HttpResponse(PERMISSION_DENIED, status=401)
    return get_json_from(get_users_registrated_json())

@login_required
def get_account_types_json_view(request):
    if not request.user.is_superuser:
        return HttpResponse(PERMISSION_DENIED, status=401)
    return get_json_from(get_account_types_json())


@login_required
def get_users_status_json_view(request):
    if not request.user.is_superuser:
        return HttpResponse(PERMISSION_DENIED, status=401)

    return get_json_from(get_users_status_json())


@login_required
def get_job_categories_json_view(request):
    if not request.user.is_superuser:
        return HttpResponse(PERMISSION_DENIED, status=401)

    return get_json_from(get_job_categories_json())


# Branch statistics
@login_required
def branch_statistics(request, branch_id, slug, user_id):
    branch = get_object_or_404(Branch, pk=branch_id)
    if not is_branch_admin(request.user, branch) or not request.user.is_superuser:
        return HttpResponse(PERMISSION_DENIED, status=401)

    # Account status color
    ACTIVE_COLOR = ACTIVE_COLOR_HEX
    ON_HOLIDAY_COLOR = ON_HOLIDAY_COLOR_HEX
    UNSUBSCRIBED_COLOR = UNSUBSCRIBED_COLOR_HEX

    # Account types colors
    MEMBER_COLOR = MEMBER_COLOR_HEX
    VERIFIED_MEMBER_COLOR = VERIFIED_MEMBER_COLOR_HEX
    NON_MEMBER_COLOR = NON_MEMBER_COLOR_HEX

    branch = get_object_or_404(Branch, pk=branch_id)

    return render(request, 'statistics/branch_statistics.html', locals())


@login_required
def get_branch_reg_users_json_view(request, branch_id, slug, user_id):
    branch = get_object_or_404(Branch, pk=branch_id)
    if not is_branch_admin(request.user, branch) or not request.user.is_superuser:
        return HttpResponse(PERMISSION_DENIED, status=401)
    return get_json_from(get_branch_users_registrated_json(branch_id))


@login_required
def get_branch_account_types_json_view(request, branch_id, slug, user_id):
    branch = get_object_or_404(Branch, pk=branch_id)
    if not is_branch_admin(request.user, branch) or not request.user.is_superuser:
        return HttpResponse(PERMISSION_DENIED, status=401)
    return get_json_from(get_branch_account_types_json(branch_id))


@login_required
def get_branch_user_status_json_view(request, branch_id, slug, user_id):
    branch = get_object_or_404(Branch, pk=branch_id)
    if not is_branch_admin(request.user, branch) or not request.user.is_superuser:
        return HttpResponse(PERMISSION_DENIED, status=401)
    return get_json_from(get_branch_user_status_json(branch_id))


@login_required
def get_branch_job_categories_json_view(request, branch_id, slug, user_id):
    branch = get_object_or_404(Branch, pk=branch_id)
    if not is_branch_admin(request.user, branch) or not request.user.is_superuser:
        return HttpResponse(PERMISSION_DENIED, status=401)
    return get_json_from(get_branch_job_categories_json(branch_id))





# Users statistics

@login_required
def get_user_job_categories_json_view(request, user_id):
    if request.user.id != int(user_id) and not request.user.is_superuser:
        return HttpResponse(PERMISSION_DENIED, status=401)

    return get_json_from(get_user_job_categories_json(user_id))


@login_required
def get_user_job_avg_time_json_view(request, user_id):
    if request.user.id != int(user_id) and not request.user.is_superuser:
        return HttpResponse(PERMISSION_DENIED, status=401)

    return get_json_from(get_user_job_avg_time_json(user_id))


@login_required
def get_user_jobs_amount_json_view(request, user_id):
    if request.user.id != int(user_id) and not request.user.is_superuser:
        return HttpResponse(PERMISSION_DENIED, status=401)

    return get_json_from(get_user_jobs_amount_json(user_id))


@login_required
def get_user_time_amount_json_view(request, user_id):
    if request.user.id != int(user_id) and not request.user.is_superuser:
        return HttpResponse(PERMISSION_DENIED, status=401)

    return get_json_from(get_user_time_amount_json(user_id))


@login_required
def get_user_km_amount_json_view(request, user_id):
    if request.user.id != int(user_id) and not request.user.is_superuser:
        return HttpResponse(PERMISSION_DENIED, status=401)

    return get_json_from(get_user_km_amount_json(user_id))


### Search ###
@login_required
def search_view(request):
    """user search in header"""
    input = request.GET.get('q')
    userlist = User.objects.filter(Q(first_name__icontains=input) | Q(last_name__icontains=input) | Q(username__icontains=input))
    return render(request, 'search/search.html', locals())

@login_required
def job_search_view(request):
    """job search in left menu"""
    form = JobSearchForm()
    if request.method == 'POST':
        form = JobSearchForm(request.POST)
        if form.is_valid():


            if not form.cleaned_data['date1']:
                date1 = timezone.now()+timezone.timedelta(hours=-25)
            else:
                date1 = form.cleaned_data['date1']

            if not form.cleaned_data['date2']:
                date2 = timezone.datetime.max
            else:
                date2 = form.cleaned_data['date2']

            if not form.cleaned_data['category']:
                category = [str(l[0]) for l in JobCategory.JOB_CATEGORIES]
                
            else:
                category = form.cleaned_data['category']

            if not form.cleaned_data['job_type']:
                job_type = [str(l[0]) for l in JobType.JOB_TYPES]
            else:
                job_type = form.cleaned_data['job_type']

            if not form.cleaned_data['receive_help_from_who']:
                receive_help_from_who = [str(l[0]) for l in MemberType.MEMBER_TYPES_GROUP]
            else:
                receive_help_from_who = form.cleaned_data['receive_help_from_who']

            if not form.cleaned_data['time']:
                time = [str(l[0]) for l in TIME_CHOICES]
            else:
                time = form.cleaned_data['time']

            request_time = Q(time__contains=time[0])
            for l in time[1:] :
                request_time |= Q(time__contains=l)

            request_category = Q(category__contains=category[0])
            for l in category[1:] :
                request_category |= Q(category__contains=l)

            if str(JobType.OFFRE) in job_type:
                offers = Offer.objects.filter(Q(date__gte=date1) &  Q(date__lte=date2) & Q(receive_help_from_who__in = receive_help_from_who) & request_time & request_category).all()

            if str(JobType.DEMAND) in job_type:
                demands = Demand.objects.filter(Q(date__gte=date1) &  Q(date__lte=date2) & Q(receive_help_from_who__in = receive_help_from_who) & request_time & request_category & Q(closed=False)).all()


            return render(request, 'search/job_result.html',locals())

    return render(request,'search/job.html', locals())

### CREDIT ###

@login_required
def credits_view(request):
    """view for credit menu and gitf"""
    user = request.user
    #TODO : Rajouter le champ finish = true dans job et offer et finish = false dans les autres.
    jobs = Demand.objects.filter(closed=True,donor=user,success=True).all() # tâches que j'ai faîtes
    offer = Demand.objects.filter(closed=True,receiver=user,success=True).all() # tâches que j'ai reçue
    jobs_pending = Demand.objects.filter(closed=True,donor=user,success=None).all() # tâches que je vais faire
    offer_pending = Demand.objects.filter(closed=True,receiver=user,success=None).all() # tâches que je vais recevoir
    num_jobs = len(jobs)
    average_time_job = 0
    km = 0      # TODO: This variable is not used (On l'affiche dans la template)
    for job in jobs :
        average_time_job += job.real_time
        km += job.km
    if num_jobs != 0:
        average_time_job = average_time_job/num_jobs
    form = GiftForm(ruser=user)
    if request.POST:
        form = GiftForm(request.POST, ruser=user)
        if form.is_valid():
            if form.cleaned_data['check'] == 1:
                friend = User.objects.get(username=form.cleaned_data['user'])
            else :
                friend = get_object_or_404(User, pk=1)
            if not friend :
                return render(request,'credit/credit_page.html.html', locals())
            friend.credit += form.cleaned_data['amount']
            user.credit -= form.cleaned_data['amount']
            user.save()
            friend.save()
            title = _("Cadeau de : {amount} minutes").format(amount=str(form.cleaned_data['amount']))
            pm_write(user, friend, title, form.cleaned_data['message'])
            return redirect('home')


    return render(request,'credit/credit_page.html', locals())

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView

from branch.models import Branch, BranchMembers, Demand, Offer, Comment, DemandProposition, SuccessDemand
from main.models import User, VerifiedInformation, JobCategory, MemberType

from branch.forms import CreateBranchForm, ChooseBranchForm, OfferHelpForm, NeedHelpForm, \
            CommentForm, UpdateNeedHelpForm, VolunteerForm, ForceVolunteerForm, SuccessDemandForm, \
            CommentConfirmForm, TakeOfferForm
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils import formats
from main.utils import can_manage, is_branch_admin, refuse, can_manage_branch_specific, is_in_branch, \
                        discriminate_demands, discriminate_offers
from postman.api import pm_write
from django.core.urlresolvers import resolve
from django.db.models import Q

@login_required
@user_passes_test(lambda u: u.is_verified)
def branch_create(request):
    """ View for creating a branch """
    user = request.user
    form = CreateBranchForm()

    if request.POST:
        form = CreateBranchForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = user
            obj.save()
            rel = BranchMembers(user=user, branch=obj, is_admin=True, joined=timezone.now())
            rel.save()
            messages.add_message(request, messages.INFO, _('Branche créée'))
            return redirect(obj.get_absolute_url())

    return render(request,'branch/branch_create.html', locals())

def branch_home(request, branch_id, slug):
    """ Display branch id information """
    branch = get_object_or_404(Branch, pk=branch_id)
    user = request.user

    bm = BranchMembers.objects.filter(branch=branch, user=user)
    is_in = bm.count()

    if is_in == 0 and not user.is_superuser:
        return refuse(request)


    if user.is_superuser:
        is_branch_admin = True
        # if superUser is not already in the branch, add him
        try:
            BranchMembers.objects.get(branch=branch, user=user)
        except BranchMembers.DoesNotExist:
            bm = BranchMembers(branch=branch, user=user, is_admin=True, joined=timezone.now())
            bm.save()
    else:
        is_branch_admin = bm.first().is_admin

    nb_users = BranchMembers.objects.filter(branch=branch).count()

    user_ids = [mb.user.id for mb in branch.membership.all()]

    if is_branch_admin:
        vdemands = VerifiedInformation.objects.filter(user__in=user_ids)
        all_usernames = ':'.join([b.user.username for b in BranchMembers.objects.filter(branch=branch)])

    demands = Demand.objects.filter(receiver__in=user_ids, branch=branch)
    offers = Offer.objects.filter(donor__in=user_ids, branch=branch)

    date_now = timezone.now() + timezone.timedelta(hours=-24)

    demands = demands.up_to_date()
    offers = offers.up_to_date()

    demands = discriminate_demands(request, demands)
    offers = discriminate_offers(request, offers)

    return render(request,'branch/branch_home.html', locals())

@user_passes_test(lambda u: not u.user_type == MemberType.NON_MEMBER)
@login_required
def branch_join(request):
    """ Rejoign a branch """
    branches = Branch.objects.all()
    form = ChooseBranchForm()
    user = request.user

    if request.POST:
        form = ChooseBranchForm(request.POST)
        if form.is_valid():
            br_id = form.cleaned_data['id']
            branch = Branch.objects.get(pk=br_id)
            if user in branch.banned.all():
                messages.add_message(request, messages.INFO, _('Vous avez été banni de la branche {branch} et ne pouvez pas la rejoindre').format(branch=branch))

            elif BranchMembers.objects.filter(branch=branch, user=user).count() > 0:
                messages.add_message(request, messages.INFO, _('Vous êtes déjà dans la branche {branch}').format(branch=branch))
            else:
                obj = BranchMembers(branch=branch, user=user, is_admin=False, joined=timezone.now())
                obj.save()
                messages.add_message(request, messages.INFO, _('Vous avez rejoins la branche {branch}').format(branch=branch))
                return redirect(branch.get_absolute_url())

    return render(request,'branch/branch_join.html', locals())

@login_required
def branch_leave(request, branch_id, user_id):
    """ Leave a branch """
    branch = get_object_or_404(Branch, pk=branch_id)
    user = get_object_or_404(User, pk=user_id)

    if can_manage(user, request.user) and user.id != branch.creator :
        try:
            to_remove = BranchMembers.objects.get(branch=branch_id, user=user_id)
            to_remove.delete()
            Demand.objects.filter(branch=branch, receiver=user, success=None, closed=False).delete()
            Offer.objects.filter(branch=branch, donor=user).delete()
            messages.add_message(request, messages.INFO, _('Vous avez quitté la branche {branch}').format(branch=branch))
        except:
            pass
    else :
        return refuse(request)

    return redirect('home')

@login_required
def branch_ban(request, branch_id, user_id):
    """ Ban an user form the branch id """
    branch = get_object_or_404(Branch, pk=branch_id)
    user = get_object_or_404(User, pk=user_id)

    if can_manage(user, request.user):
        try:
            to_remove = BranchMembers.objects.get(branch=branch_id, user=user_id)
            to_remove.delete()
            branch.banned.add(to_remove.user)
        except:
            pass

        subject = _('Bannissement de la branche {branch}').format(branch=branch.name)
        body = _('Vous avez été banni de la branche {branch}. Vous ne pouvez à présent plus rejoindre cette branche. Pour plus d\'informations, contactez un adminstrateur ou l\'officier en charge de la branche en question').format(branch=branch.name)
        pm_write(request.user, user, subject, body)
        messages.add_message(request, messages.INFO, _('{user} a été banni de la branche {branch}').format(branch=branch, user=user))

        Offer.objects.filter(branch=branch, donor=user).delete()
        Demand.objects.filter(branch=branch, receiver=user, success=None, closed=False).delete()

    else :
        return refuse(request)

    return redirect(branch.get_absolute_url())

@login_required
def branch_unban(request, branch_id, user_id):
    """ Unban an user from the branch admin """
    branch = get_object_or_404(Branch, pk=branch_id)
    user = get_object_or_404(User, pk=user_id)

    try:
        to_unban = User.objects.get(id=user_id)
        branch.banned.remove(to_unban)
        subject = _('Annulation du bannissement de la branche {branch}').format(branch=branch.name)
        body = _('Nous avons annulé le bannissement de la branche {branch} vous concernant. Vous pouvez à présent rejoindre cette branche si vous le souhaitez.').format(branch=branch.name)
        pm_write(request.user, user, subject, body)
        messages.add_message(request, messages.INFO, _('le bannissement de {user} dans la branche {branch} a été annulé').format(branch=branch, user=user))
    except:
        pass

    return redirect(branch.get_absolute_url())

@login_required
def branch_promote(request, branch_id, user_id):
    """ Promote (admin) the user_id in branch_id """
    branch = get_object_or_404(Branch, pk=branch_id)
    user = get_object_or_404(User, pk=user_id)

    if is_branch_admin(request.user, branch) or request.user.is_superuser:
        try:
            to_promote = BranchMembers.objects.get(branch=branch_id, user=user_id)
            to_promote.is_admin = True
            to_promote.save()
            messages.add_message(request, messages.INFO, _('{user} a été promu administrateur de la branche {branch}').format(branch=branch, user=user))
        except:
            pass
    else :
        return refuse(request)

    return redirect(branch.get_absolute_url())

@login_required
def branch_demote(request, branch_id, user_id):
    """ Demote the user_id on branch_id """
    branch = get_object_or_404(Branch, pk=branch_id)
    user = get_object_or_404(User, pk=user_id)

    if is_branch_admin(request.user, branch) or request.user.is_superuser:
        try:
            to_demote = BranchMembers.objects.get(branch=branch_id, user=user_id)
            to_demote.is_admin = False
            to_demote.save()
            messages.add_message(request, messages.INFO, _('{user} n\'est plus administrateur de la branche {branch}').format(branch=branch, user=user))
        except:
            pass
    else :
        return refuse(request)
    return redirect(branch.get_absolute_url())


@login_required
def branch_delete(request, branch_id):
    """ Delete a branch """
    branch = get_object_or_404(Branch, pk=branch_id)

    if request.user == branch.creator or request.user.is_superuser:
        try:
            branch.delete()
            messages.add_message(request, messages.INFO, _('Vous avez supprimé la branche {branch}').format(branch=branch))
        except:
            pass
    else:
        return refuse(request)
    return redirect('home')

@login_required
def delete_demand(request, branch_id, slug, demand_id):
    """ Delete a demand """
    demand = get_object_or_404(Demand, pk=demand_id)

    if can_manage_branch_specific(demand.receiver, request.user, demand.branch):
       demand.delete()
       messages.add_message(request, messages.INFO, _('Vous avez supprimé la demande {demand}').format(demand=demand))
       return redirect(demand.branch.get_absolute_url())
    else:
        return refuse(request)

@login_required
def delete_offer(request, branch_id, slug, offer_id):
    """ Delete an offer """
    offer = get_object_or_404(Offer, pk=offer_id)

    if can_manage_branch_specific(offer.donor, request.user, offer.branch):
       offer.delete()
       messages.add_message(request, messages.INFO, _('Vous avez supprimé l\'offre {offer}').format(offer=offer))
       return redirect(offer.branch.get_absolute_url())
    return redirect('home')

@login_required
def volunteer_decline(request, volunteer_id):
    """ Decline an help form the volunteer_id """
    demandProposition = DemandProposition.objects.get(pk=volunteer_id)
    demand = demandProposition.demand

    if can_manage_branch_specific(demand.receiver, request.user, demand.branch):
        demandProposition.delete()
        messages.add_message(request, messages.INFO, _('Vous avez refusé cette aide'))
        return redirect(demand.get_absolute_url())
    return redirect('home')

@login_required
def volunteer_accept(request, volunteer_id):
    """ Accept an help from the volunteer_id """
    demandProposition = DemandProposition.objects.get(pk=volunteer_id)
    demand = demandProposition.demand

    if can_manage_branch_specific(demand.receiver, request.user, demand.branch):
        demandProposition.accepted = True
        demandProposition.save()

        subject = _("Je vous ai choisi pour '") + demand.title + "'"
        body = _(" Je vous ai choisi pour effectuer le job '") + demand.title + "'"
        body += '\n\n' + _('Lieu : ') + demand.location
        body += '\n' + _('Date : ') + formats.date_format(demand.date, "DATE_FORMAT")
        body += '\n' + _('Heure(s) désirée(s) : ') + demand.get_verbose_time()
        body += '\n' + _('Description : ') + demand.description

        body += '\n'
        if demand.receiver.emergency_contacts.count() > 0:
            body += '\n' + _('En cas d\'incident durant cette tâche, voici les personnes à contacter :')
            for ec in demand.receiver.emergency_contacts.all():
                body += '\n' + _('Prénom :') + ' ' + ec.first_name
                body += '\n' + _('Nom :') + ' ' + ec.last_name
                body += '\n' + _('Téléphone fixe :') + ' ' + ec.phone_number
                body += '\n' + _('Téléphone mobile :') + ' ' + ec.mobile_number
                body += '\n' + _('Langues parlées :') + ' ' + ec.get_verbose_languages()
                body += '\n'

        body += '\n\n' + _('N\'hésitez pas à me contacter pour de plus amples informations')
        body += '\n' + _('À bientôt,') + '\n'
        body += demand.receiver.first_name

        pm_write(demand.receiver, demandProposition.user, subject, body)

        for vol in DemandProposition.objects.filter(demand=demand, accepted=False):
            vol.delete()

        demand.closed = True
        demand.km = demandProposition.km
        if not demand.km:
            demand.km = 0
        demand.donor = demandProposition.user
        demand.save()

        messages.add_message(request, messages.INFO, _('Vous avez accepté cette aide !'))
        return redirect(demand.get_absolute_url())
    return redirect('home')

class CreateDemandView(CreateView):
    """
    A registration backend for our CareRegistrationForm
    """
    template_name = 'job/need_help.html'
    form_class = NeedHelpForm
    model = Demand

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not is_in_branch(User.objects.get(pk=self.kwargs['user_id']),
            Branch.objects.get(pk=self.kwargs['branch_id'])):
            return refuse(self.request)
        return super(CreateDemandView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateDemandView, self).get_context_data(**kwargs)
        context['ruser'] = User.objects.get(pk=self.kwargs['user_id'])
        context['branch'] = Branch.objects.get(pk=self.kwargs['branch_id'])
        return context

    def get_initial(self):
        ruser = User.objects.get(pk=self.kwargs['user_id'])
        return {'receive_help_from_who': ruser.receive_help_from_who,
                'location': ruser.location,
                'latitude': ruser.latitude,
                'longitude': ruser.longitude}

    def form_valid(self, form):
        form.instance.branch = Branch.objects.get(pk=self.kwargs['branch_id'])
        form.instance.receiver = User.objects.get(pk=self.kwargs['user_id'])
        form.instance.real_time = form.instance.estimated_time
        return super(CreateDemandView, self).form_valid(form)

    def get_success_url(self):
        date = self.object.date
        find_offers = Offer.objects.filter(date=date)

        category = self.object.category
        request_time = Q(time__contains=self.object.time[0])
        for r in self.object.time[1:]:
            request_time |= Q(time__contains=r)
        request_category = Q(category__contains=category[0])

        find_offers = find_offers.filter(request_time & request_category).all()
        find_offers = discriminate_offers(self.request, find_offers)

        for offer in find_offers:
            subject = _("Une correspondance a été trouvée !")
            body1 = _("Nous avons trouvé une demande correspondant à une de vos offre d'aide !\nCette demande d'aide a été faite par l'utilisateur {user} ({username}) et a pour titre {title}.\n"
                "Vous pouvez consulter cette demande et vous proposer comme volontaire en suivant ce lien :\nhttp://{meta}{link}\n"
                "Si vous décidez de vous proposez pour cette demande et que votre offre d'aide n'est donc plus valable,"
                " vous pouvez annuler votre offre d'aide via la page d'accueil de votre branche ou la page d'accueil du site.")\
            .format(user=self.object.receiver.get_full_name(), title=self.object.title, link=self.object.get_absolute_url(), username=self.object.receiver, meta=self.request.META['HTTP_HOST'])

            pm_write(self.object.receiver, offer.donor, subject, body1)

            body2 = _("Nous avons trouvé une offre correspondant à une de vos demande d'aide !\nCette offre d'aide a été faite par l'utilisateur {user} ({username}) et correspond a votre demande {title}.\n"
                "Un message automatique a été envoyé à {user} ({username}) pour l'informer de cette correspondance et celui-ci devrait se proposer comme volontaire pour votre demande sous peu.")\
            .format(user=offer.donor.get_full_name(), title=self.object.title, username=offer.donor)

            pm_write(offer.donor, self.object.receiver, subject, body2)
        return self.object.get_absolute_url()

class TakeOfferDemandView(CreateDemandView):
    form_class = TakeOfferForm
    template_name = 'job/take_offer.html'

    def form_valid(self, form):
        form.instance.date = Offer.objects.get(pk=self.kwargs['offer_id']).date
        return super(TakeOfferDemandView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TakeOfferDemandView, self).get_context_data(**kwargs)
        offer = Offer.objects.get(pk=self.kwargs['offer_id'])
        context['offer'] = offer
        category_keep = []
        for cat in offer.category:
            if cat == 'a':
                category_keep.append(10)
            elif cat == 'b':
                category_keep.append(11)
            else :
                category_keep.append(cat)
        context['category_keep'] = category_keep
        return context

class UpdateDemandView(UpdateView):
    """
    A registration backend for our CareRegistrationForm
    """
    template_name = 'job/need_help.html'
    form_class = UpdateNeedHelpForm
    model = Demand

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        if not can_manage_branch_specific(obj.receiver, self.request.user, obj.branch):
            return refuse(self.request)
        return super(UpdateDemandView, self).dispatch(*args, **kwargs)

    def get_object(self):
        return Demand.objects.get(pk=self.kwargs['demand_id'])

    def get_context_data(self, **kwargs):
        context = super(UpdateDemandView, self).get_context_data(**kwargs)
        context['ruser'] = self.get_object().receiver
        context['branch'] = self.get_object().branch
        context['update'] = True
        return context

    def form_valid(self, form):
        return super(UpdateDemandView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()

class UpdateOfferView(UpdateView):
    """
    A registration backend for our CareRegistrationForm
    """
    template_name = 'job/offer_help.html'
    form_class = OfferHelpForm
    model = Offer

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        if not can_manage_branch_specific(obj.donor, self.request.user, obj.branch):
            return refuse(self.request)
        return super(UpdateOfferView, self).dispatch(*args, **kwargs)

    def get_object(self):
        return Offer.objects.get(pk=self.kwargs['offer_id'])

    def get_context_data(self, **kwargs):
        context = super(UpdateOfferView, self).get_context_data(**kwargs)
        context['ruser'] = self.get_object().receiver
        context['branch'] = self.get_object().branch
        context['update'] = True
        return context

    def form_valid(self, form):
        return super(UpdateOfferView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class CreateOfferView(CreateView):
    """
    A registration backend for our CareRegistrationForm
    """
    template_name = 'job/offer_help.html'
    form_class = OfferHelpForm
    model = Offer

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not is_in_branch(User.objects.get(pk=self.kwargs['user_id']),
            Branch.objects.get(pk=self.kwargs['branch_id'])):
            return refuse(self.request)
        return super(CreateOfferView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateOfferView, self).get_context_data(**kwargs)
        context['ruser'] = User.objects.get(pk=self.kwargs['user_id'])
        context['branch'] = Branch.objects.get(pk=self.kwargs['branch_id'])
        return context

    def form_valid(self, form):
        form.instance.branch = Branch.objects.get(pk=self.kwargs['branch_id'])
        form.instance.donor = User.objects.get(pk=self.kwargs['user_id'])
        return super(CreateOfferView, self).form_valid(form)

    def get_success_url(self):
        return Branch.objects.get(pk=self.kwargs['branch_id']).get_absolute_url()

class DetailOfferView(CreateView): # This view is over-hacked. Don't take it as a reference.
    """
    Detail view for a Offer
    """
    template_name = 'job/details_offer.html'
    model = Comment
    form_class = CommentForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not is_in_branch(self.request.user, self.get_object().branch):
            return refuse(self.request)
        return super(DetailOfferView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return Offer.objects.get(pk=self.kwargs['offer_id'])

    def get_context_data(self, **kwargs):
        context = super(DetailOfferView, self).get_context_data(**kwargs)
        obj = self.get_object()
        context['object'] = obj
        if can_manage_branch_specific(obj.donor, self.request.user, obj.branch):
            context['can_manage'] = True
        return context

    def form_valid(self, form):
        form.instance.content_object = self.get_object()
        form.instance.user = self.request.user

        return super(DetailOfferView, self).form_valid(form)

    def get_success_url(self):

        subject = self.request.user.get_full_name() + ' ' + _("a commenté votre offre")
        body = self.request.user.get_full_name() + ' ' + _("a commenté votre offre")
        body += '\n\n' + _('Commentaire : ') + self.object.comment
        body += '\n\n' + _('Vous pouvez lui répondre en vous rendant sur votre offre :')
        body += '\n' + 'http://' + self.request.META['HTTP_HOST'] + self.get_object().get_absolute_url()

        pm_write(self.request.user, self.get_object().donor, subject, body)

        return self.get_object().get_absolute_url() + '#' + str(self.object.id)

class DetailDemandView(CreateView): # This view is over-hacked. Don't take it as a reference.
    """
    Detail view for a Demand
    """
    template_name = 'job/details_demand.html'
    model = Comment
    form_class = CommentForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not is_in_branch(self.request.user, self.get_object().branch):
            return refuse(self.request)
        if not self.request.user.is_superuser and self.request.user in self.get_object().receiver.ignore_list.all():
            return refuse(self.request)
        return super(DetailDemandView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return Demand.objects.get(pk=self.kwargs['demand_id'])

    def get_context_data(self, **kwargs):
        context = super(DetailDemandView, self).get_context_data(**kwargs)
        obj = self.get_object()
        context['object'] = obj
        if self.request.user in obj.volunteers.all():
            context['already_volunteer'] = True
        if can_manage_branch_specific(obj.receiver, self.request.user, obj.branch):
            context['can_manage'] = True
        return context

    def form_valid(self, form):
        form.instance.content_object = self.get_object()
        form.instance.user = self.request.user
        return super(DetailDemandView, self).form_valid(form)

    def get_success_url(self):

        subject = self.request.user.get_full_name() + ' ' + _("a commenté votre demande '") + self.get_object().title + '\''
        body = self.request.user.get_full_name() + ' ' + _("a commenté votre demande '") + self.get_object().title + '\''
        body += '\n\n' + _('Commentaire : ') + self.object.comment
        body += '\n\n' + _('Vous pouvez lui répondre en vous rendant sur votre demande:')
        body += '\n' + 'http://' + self.request.META['HTTP_HOST'] + self.get_object().get_absolute_url()

        pm_write(self.request.user, self.get_object().receiver, subject, body)

        return self.get_object().get_absolute_url() + '#' + str(self.object.id)

class CreateVolunteerView(CreateView):
    """
    A registration backend for our CareRegistrationForm
    """
    template_name = 'job/volunteer_demand.html'
    model = DemandProposition
    form_class = VolunteerForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateVolunteerView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.demand = Demand.objects.get(pk=self.kwargs['demand_id'])
        form.instance.user = User.objects.get(pk=self.kwargs['volunteer_id'])
        return super(CreateVolunteerView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateVolunteerView, self).get_context_data(**kwargs)
        demand = Demand.objects.get(pk=self.kwargs['demand_id'])
        context['demand'] = demand
        context['possible_time'] = demand.time
        return context

    def get_initial(self):
        return {'km': self.request.GET.get('km', 0),}

    def get_success_url(self):
        demand = Demand.objects.get(pk=self.kwargs['demand_id'])
        volunteer = self.object.user

        subject = volunteer.get_full_name() + ' ' + _("vous offre son aide pour '") + demand.title + "'"
        body = volunteer.get_full_name() + ' ' + _("vous offre son aide pour '") + demand.title + "'"
        body += '\n\n' + _('Commentaire : ') + self.object.comment
        body += '\n' + _('Km de chez vous : ') + str(self.object.km)
        body += '\n' + _('Heure(s) choisies(s) : ') + self.object.get_verbose_time()
        body += '\n\n' + _('Vous pouvez accepter son offre d\'aide en vous rendant sur votre demande d\'aide:')
        body += '\n' + 'http://' + self.request.META['HTTP_HOST'] + demand.get_absolute_url()

        pm_write(volunteer, demand.receiver, subject, body)

        return demand.get_absolute_url()

class ForceCreateVolunteerView(CreateVolunteerView):
    form_class = ForceVolunteerForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        demand = Demand.objects.get(pk=self.kwargs['demand_id'])
        if not can_manage_branch_specific(demand.receiver, self.request.user, demand.branch):
            return refuse(self.request)
        return super(CreateVolunteerView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ForceCreateVolunteerView, self).get_context_data(**kwargs)
        context['form'].fields['user'].queryset = context['demand'].branch.members.all()
        return context

    def form_valid(self, form):
        demand = Demand.objects.get(pk=self.kwargs['demand_id'])
        form.instance.demand = demand
        return super(CreateVolunteerView, self).form_valid(form) #correct

class CreateSuccessDemand(CreateView):
    form_class = SuccessDemandForm
    template_name = 'job/success_demand.html'
    model = SuccessDemand

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateSuccessDemand, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        demand = Demand.objects.get(pk=self.kwargs['demand_id'])
        form.instance.demand = demand
        form.instance.asked_by = demand.donor
        form.instance.ask_to = demand.receiver
        form.instance.branch = demand.branch
        demand.success_fill = True
        demand.save()
        return super(CreateSuccessDemand, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateSuccessDemand, self).get_context_data(**kwargs)
        context['demand'] = Demand.objects.get(pk=self.kwargs['demand_id'])
        return context

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('Demande envoyée'))

        subject = _("Confirmation de job accompli")
        body = _("L'utilisateur {user} ({username}) affirme avoir accompli le job suivant : {job}.\nIl déclare avoir pris {time} minutes pour accomplir ce job.\n"
            "Si ces informations vous semble correctes, vous pouvez confirmer que ce job a été accompli avec succès.")\
        .format(user=self.object.asked_by.get_full_name(), job=self.object.demand.title, time=self.object.time, username=self.object.asked_by)
        pm_write(self.object.asked_by, self.object.ask_to, subject, body)
        return reverse('home')


def unsuccess_job(request, demand_id):
    """ View for a job who has not been completed """
    demand = get_object_or_404(Demand, pk=demand_id)

    if can_manage_branch_specific(demand.donor, request.user, demand.branch):
       demand.success_fill=True
       demand.success=False
       demand.save()

       subject = _("Absence lors d'un job")
       body = _("L'utilisateur {user} ({username}) n'était apparemment pas présent pour accomplir le job {job}.\n"
        "S'il s'agit d'une erreur et que {user} ({username}) était bien présent, veuillez contacter un administrateur pour régler le problème.\n"
        "Si vous désirez ne plus demander d'aide à l'utilisateur {user} ({username}), vous pouvez l'ignorer en vous rendant sur son profil.")\
       .format(user=demand.donor.get_full_name(), job=demand.title, username=demand.donor)
       pm_write(demand.donor, demand.receiver, subject, body)

       messages.add_message(request, messages.INFO, _('Vous avez indiqué la tâche {demand} comme non-completée').format(demand=demand))
       return redirect('home')
    else:
        return refuse(request)

def manage_success(request, success_demand_id):
    """ View for a job who has been completed """
    success = get_object_or_404(SuccessDemand, pk=success_demand_id)
    demand = success.demand

    form = CommentConfirmForm()

    if can_manage_branch_specific(success.ask_to, request.user, success.branch):
        if request.POST:
            form = CommentConfirmForm(request.POST)
            if form.is_valid():
                if 'accept' in request.POST:
                    if success.time > 100000:
                        success.time = 100000
                    if success.time < 0:
                        success.time = 0

                    demand.real_time =  success.time
                    demand.success = True


                    demand.donor.credit += success.time
                    demand.donor.save()
                    demand.receiver.credit -= success.time
                    demand.receiver.save()

                    subject = _("Job confirmé")
                    body = _("L'utilisateur {user} ({username}) a confirmé que vous aviez accompli le job {job} avec succès ! Votre compte a donc été crédité de {time} minutes.\n")\
                    .format(user=demand.receiver.get_full_name(), job=demand.title, time=success.time, username=demand.receiver)
                    if form.cleaned_data['comment'] != "":
                        body += _("L'utilisateur {user} ({username}) a laissé le commentaire suivant : {comment}")\
                        .format(user=demand.receiver.get_full_name(), comment=form.cleaned_data['comment'], username=demand.receiver)
                    pm_write(demand.receiver, demand.donor, subject, body)
                    success.delete()
                    demand.save()

                    return redirect('home')
                if 'decline' in request.POST:
                    success.delete()
                    demand.success_fill = False
                    demand.save()

                    subject = _("Job refusé")
                    body = _("L'utilisateur {user} ({username}) a déclaré que vous n'aviez pas passé {time} minutes pour accomplir le job {job}. Votre compte n'a donc pas été crédité.\n")\
                    .format(user=demand.receiver.get_full_name(), job=demand.title, time=success.time, username=demand.receiver)
                    if form.cleaned_data['comment'] != "":
                        body += _("L'utilisateur {user} ({username}) a laissé un commentaire, expliquant pourquoi il n'a pas désiré créditer votre compte : {comment}\n"
                        "Vous pouvez recréer une demande de confirmation avec un nouveau montant de crédit correspondant plus à la perception du demandeur d'aide.\n"
                        "Si vous ne parvenez pas à trouver un terrain d'entente avec l'utilisateur {user} ({username}), vous pouvez contacter un administrateur pour régler le problème.")\
                        .format(user=demand.receiver.get_full_name(), comment=form.cleaned_data['comment'], username=demand.receiver)
                    pm_write(demand.receiver, demand.donor, subject, body)

                    return redirect('home')

        return render(request,'job/manage_success.html', locals())

    else :
        return refuse(request)

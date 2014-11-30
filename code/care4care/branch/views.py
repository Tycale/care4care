from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.contrib import messages

from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from branch.models import Branch, BranchMembers, Demand, Offer, Comment

from main.models import User, VerifiedInformation

from branch.forms import CreateBranchForm, ChooseBranchForm, OfferHelpForm, NeedHelpForm, CommentForm
from django.utils import timezone
from django.core.urlresolvers import reverse

@login_required
@user_passes_test(lambda u: u.is_verified)
def branch_create(request):
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
    branch = get_object_or_404(Branch, pk=branch_id)
    user = request.user

    bm = BranchMembers.objects.filter(branch=branch, user=user)
    is_in = bm.count()

    if is_in == 0 and not user.is_superuser:
        messages.add_message(request, messages.INFO, _("Vous n'avez rien à faire ici !"))
        return redirect('home')


    if user.is_superuser:
        is_branch_admin = True
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

    demands = Demand.objects.filter(receiver__in=user_ids, branch=branch)
    offers = Offer.objects.filter(donor__in=user_ids, branch=branch)

    return render(request,'branch/branch_home.html', locals())

@login_required
def branch_join(request):
    branches = Branch.objects.all()
    form = ChooseBranchForm()
    user = request.user

    if request.POST:
        form = ChooseBranchForm(request.POST)
        if form.is_valid():
            br_id = form.cleaned_data['id']
            branch = Branch.objects.get(pk=br_id)
            if BranchMembers.objects.filter(branch=branch, user=user).count() > 0:
                messages.add_message(request, messages.INFO, _('Vous êtes déjà dans la branche {branch}').format(branch=branch))
            else:
                obj = BranchMembers(branch=branch, user=user, is_admin=False, joined=timezone.now())
                obj.save()
                messages.add_message(request, messages.INFO, _('Vous avez rejoins la branche {branch}').format(branch=branch))
                return redirect(branch.get_absolute_url())

    return render(request,'branch/branch_join.html', locals())

@login_required
def branch_leave(request, branch_id, user_id):
    branch = get_object_or_404(Branch, pk=branch_id)
    user = get_object_or_404(User, pk=user_id)

    if user == request.user or request.user == branch.creator or request.user.is_superuser:
        try:
            to_remove = BranchMembers.objects.get(branch=branch_id, user=user_id)
            to_remove.delete()
            if user != request.user:
                messages.add_message(request, messages.INFO, _('Vous avez quitté la branche {branch}').format(branch=branch))
            else:
                messages.add_message(request, messages.INFO, _('{user} a été retiré de la branche {branch}').format(branch=branch, user=user))
        except:
            pass
    
    return redirect('home')


@login_required
def branch_delete(request, branch_id):
    branch = get_object_or_404(Branch, pk=branch_id)

    if request.user == branch.creator or request.user.is_superuser:
        try:
            branch.delete()
            messages.add_message(request, messages.INFO, _('Vous avez supprimé la branche {branch}').format(branch=branch))
        except:
            pass
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
        return super(CreateDemandView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateDemandView, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs['user_id'])
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
        #form.instance.real_time = form.instance.estimated_time
        return super(CreateDemandView, self).form_valid(form)

    def get_success_url(self):
        return Branch.objects.get(pk=self.kwargs['branch_id']).get_absolute_url()


class CreateOfferView(CreateView):
    """
    A registration backend for our CareRegistrationForm
    """
    template_name = 'job/offer_help.html'
    form_class = OfferHelpForm
    model = Offer

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateOfferView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateOfferView, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs['user_id'])
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

    def get_object(self, queryset=None):
        return Offer.objects.get(pk=self.kwargs['offer_id'])

    def get_context_data(self, **kwargs):
        context = super(DetailOfferView, self).get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context

    def form_valid(self, form):
        form.instance.content_object = self.get_object()
        form.instance.user = self.request.user
        return super(DetailOfferView, self).form_valid(form)

    def get_success_url(self):
        return self.get_object().get_absolute_url() + '#' + str(self.object.id)

class DetailDemandView(CreateView): # This view is over-hacked. Don't take it as a reference.
    """
    Detail view for a Demand
    """
    template_name = 'job/details_demand.html'
    model = Comment
    form_class = CommentForm

    def get_object(self, queryset=None):
        return Demand.objects.get(pk=self.kwargs['demand_id'])

    def get_context_data(self, **kwargs):
        context = super(DetailDemandView, self).get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context

    def form_valid(self, form):
        form.instance.content_object = self.get_object()
        form.instance.user = self.request.user
        return super(DetailDemandView, self).form_valid(form)

    def get_success_url(self):
        return self.get_object().get_absolute_url() + '#' + str(self.object.id)

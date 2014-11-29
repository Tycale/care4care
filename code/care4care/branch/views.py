from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.contrib import messages

from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from branch.models import Branch, BranchMembers
from branch.forms import NeedHelpForm, Job

from main.models import User, VerifiedInformation

from branch.forms import CreateBranchForm, ChooseBranchForm
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

    return render(request,'branch/branch_create.html',locals())


def branch_home(request, id, slug):
    branch = get_object_or_404(Branch, pk=id)
    user = request.user

    bm = BranchMembers.objects.filter(branch=branch, user=user)
    is_in = bm.count()

    if is_in == 0 and not user.is_superuser :
        messages.add_message(request, messages.INFO, _("Vous n'avez rien à faire ici !"))
        return redirect('home')


    if user.is_superuser :
        is_branch_admin = True
        try:
            BranchMembers.objects.get(branch=branch, user=user)
        except BranchMembers.DoesNotExist:
            bm = BranchMembers(branch=branch, user=user, is_admin=True, joined=timezone.now())
            bm.save()
    else : 
        is_branch_admin = bm.first().is_admin
        
    nb_users = BranchMembers.objects.filter(branch=branch).count()


    if is_branch_admin:

        user_ids = [mb.user.id for mb in branch.membership.all()]
        vdemands = VerifiedInformation.objects.filter(user__in = user_ids )

    demands = Job.objects.filter(receiver__in=user_ids, donor=None, branch=branch)
    offers = Job.objects.filter(donor__in=user_ids, receiver=None, branch=branch)

    return render(request,'branch/branch_home.html',locals())

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
            if BranchMembers.objects.filter(branch=branch, user=user).count() > 0 :
                messages.add_message(request, messages.INFO, _('Vous êtes déjà dans la branche {branch}').format(branch=branch))
            else :
                obj = BranchMembers(branch=branch, user=user, is_admin=False, joined=timezone.now())
                obj.save()
                messages.add_message(request, messages.INFO, _('Vous avez rejoins la branche {branch}').format(branch=branch))
                return redirect(branch.get_absolute_url())

    return render(request,'branch/branch_join.html',locals())

@login_required
def branch_leave(request, branch_id, user_id):
    branch = get_object_or_404(Branch, pk=branch_id)
    user = get_object_or_404(User, pk=user_id)

    if user == request.user or request.user == branch.creator or request.user.is_superuser:
        try:
            to_remove = BranchMembers.objects.get(branch=branch_id, user=user_id)
            to_remove.delete()
            if user != request.user :
                messages.add_message(request, messages.INFO, _('Vous avez quitté la branche {branch}').format(branch=branch))
            else :
                messages.add_message(request, messages.INFO, _('{user} a été retiré de la branche {branch}').format(branch=branch, user=user))
        except:
            pass
    
    return redirect('home')


@login_required
def branch_delete(request, branch_id):
    branch = get_object_or_404(Branch, pk=branch_id)

    if request.user == branch.creator or request.user.is_superuser :
        try:
            branch.delete()
            messages.add_message(request, messages.INFO, _('Vous avez supprimé la branche {branch}').format(branch=branch))
        except:
            pass
    
    return redirect('home')

class NeedHelpView(CreateView):
    """
    A registration backend for our CareRegistrationForm
    """
    template_name = 'job/need_help.html'
    form_class = NeedHelpForm
    model = Job

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NeedHelpView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NeedHelpView, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs['user_id'])
        context['branch'] = Branch.objects.get(pk=self.kwargs['branch_id'])
        return context

    def get_initial(self):
        ruser = User.objects.get(pk=self.kwargs['user_id'])
        return {'receive_help_from_who': 
                    ruser.receive_help_from_who,
                'location': ruser.location,}

    def form_valid(self, form):
        form.instance.branch = Branch.objects.get(pk=self.kwargs['branch_id'])
        form.instance.receiver = User.objects.get(pk=self.kwargs['user_id'])
        form.instance.real_time = form.instance.estimated_time
        form.instance.latitude = form.instance.receiver.latitude
        form.instance.longitude = form.instance.receiver.longitude
        return super(NeedHelpView, self).form_valid(form)
    
    def get_success_url(self):
        return Branch.objects.get(pk=self.kwargs['branch_id']).get_absolute_url()

class DetailJobView(DetailView):
    """
    Detail view for a Job
    """
    template_name = 'job/details_job.html'
    model = Job

    def get_object(self, queryset=None):
        return Job.objects.get(pk=self.kwargs['job_id'])


class OfferHelpView(CreateView):
    """
    A registration backend for our CareRegistrationForm
    """
    template_name = 'job/offer_help.html'
    form_class = NeedHelpForm
    model = Job

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(OfferHelpView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OfferHelpView, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs['user_id'])
        context['branch'] = Branch.objects.get(pk=self.kwargs['branch_id'])
        return context

    def form_valid(self, form):
        form.instance.branch = Branch.objects.get(pk=self.kwargs['branch_id'])
        form.instance.donor = self.request.user
        form.instance.real_time = form.instance.estimated_time
        form.instance.latitude = form.instance.donor.latitude
        form.instance.longitude = form.instance.donor.longitude
        form.instance.is_offer = True
        return super(OfferHelpView, self).form_valid(form)

    def get_success_url(self):
        return Branch.objects.get(pk=self.kwargs['branch_id']).get_absolute_url()


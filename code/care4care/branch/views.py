from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import ugettext as _
from django.contrib import messages

from branch.models import Branch, BranchMembers

from main.models import User

from branch.forms import CreateBranchForm, ChooseBranchForm
from django.utils import timezone

@login_required
@user_passes_test(lambda u: u.is_verified)
def branch_create(request):
    user = request.user
    form = CreateBranchForm()

    if request.POST :
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

    is_in = BranchMembers.objects.filter(branch=branch, user=user).count

    if is_in == 0 and not user.is_superuser :
        messages.add_message(request, messages.INFO, _("Vous n'avez rien à faire ici !"))
        return redirect('home')
        
    nb_users = BranchMembers.objects.filter(branch=branch).count()

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

    if user == request.user or request.user == branch.creator or request.user.is_superuser :
        try :
            to_remove = BranchMembers.objects.get(branch=branch_id, user=user_id)
            to_remove.delete()
            if user != request.user :
                messages.add_message(request, messages.INFO, _('Vous avez quitté la branche {branch}').format(branch=branch))
            else :
                messages.add_message(request, messages.INFO, _('{user} a été retiré de la branche {branch}').format(branch=branch, user=user))
        except :
            pass
    
    return redirect('home')


@login_required
def branch_delete(request, branch_id):
    branch = get_object_or_404(Branch, pk=branch_id)

    if request.user == branch.creator or request.user.is_superuser :
        try :
            branch.delete()
            messages.add_message(request, messages.INFO, _('Vous avez supprimé la branche {branch}').format(branch=branch))
        except :
            pass
    
    return redirect('home')




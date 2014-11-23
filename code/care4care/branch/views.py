from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from branch.forms import CreateBranchForm
from django.utils.translation import ugettext as _
from django.contrib import messages

from branch.models import Branch, BranchMembers

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

	return render(request,'branch/branch_home.html',locals())

def branch_join(request):
    branches = Branch.objects.all()
    return render(request,'branch/branch_join.html',locals())

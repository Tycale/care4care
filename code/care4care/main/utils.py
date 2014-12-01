from branch.models import Branch, BranchMembers
from main.models import User
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.shortcuts import redirect

def is_branch_admin(user, branch):
	try:
		BranchMembers.objects.get(is_admin=True, user=user, branch=branch)
	except:
		return False
	return True

def is_in_branch(user, branch):
	try:
		BranchMembers.objects.get(user=user, branch=branch)
	except:
		return False
	return True

def can_manage(user_to_manage, user_admin):
	if user_admin.is_superuser:
		return True
	if user_to_manage.id == user_admin.id:
		return True
	if not user_admin.is_verified:
		return False
	branch_ids_user = user_to_manage.membership.values_list('branch_id', flat=True).all()
	branch_ids_admin = user_admin.membership.values_list('branch_id', flat=True).filter(is_admin=True)
	if len(set(branch_ids_user) & set(branch_ids_admin)) >= 1:
		return True
	return False

def can_manage_branch_specific(user_to_manage, user_admin, branch):
	if user_admin.is_superuser:
		return True
	if user_to_manage.id == user_admin.id:
		return True
	if not user_admin.is_verified:
		return False
	return is_branch_admin(user_admin, branch)

def refuse(request):
	messages.add_message(request, messages.INFO, _('REFUS'))
	return redirect('home')
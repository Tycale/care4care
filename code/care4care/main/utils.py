from branch.models import Branch, BranchMembers
from main.models import User
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.shortcuts import redirect
from main.models import JobCategory, MemberType

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

def discriminate_demands(request, demands):
    if request.user.is_superuser:
        messages.add_message(request, messages.INFO, _('Vous êtes administrateur, vous pouvez voir toutes les demandes.'))
        return demands
    if demands.first() and is_branch_admin(request.user, demands.first().branch):
        messages.add_message(request, messages.INFO, _('Vous êtes administrateur de la branche, vous pouvez voir toutes les demandes.'))
        return demands

    exclude_demand_ids = []
    for demand in demands :
        if demand.receiver in request.user.ignore_list.all():
            exclude_demand_ids.append(demand.id)
        if request.user in demand.receiver.ignore_list.all():
            exclude_demand_ids.append(demand.id)

        if demand.receive_help_from_who == MemberType.ALL:
            continue
        elif demand.receive_help_from_who == MemberType.VERIFIED_MEMBER:
            if not request.user.is_verified:
                exclude_demand_ids.append(demand.id)
        elif demand.receive_help_from_who == MemberType.FAVORITE:
            if not request.user.verified_favorites.filter(user=demand.receiver).exists():
                exclude_demand_ids.append(demand.id)

        if demand.receiver.id == request.user.id:
            if demand.id in exclude_demand_ids:
                exclude_demand_ids.remove(demand.id)
        
    demands = demands.exclude(id__in=exclude_demand_ids)
    return demands

def discriminate_offers(request, offers):
    if request.user.is_superuser:
        messages.add_message(request, messages.INFO, _('Vous êtes administrateur, vous pouvez voir toutes les offres.'))
        return offers
    if offers.first() and is_branch_admin(request.user, offers.first().branch):
        messages.add_message(request, messages.INFO, _('Vous êtes administrateur de la branche, vous pouvez voir toutes les offres.'))
        return offers

    exclude_offer_ids = []
    for offer in offers :
        if offer.donor in request.user.ignore_list.all():
            exclude_offer_ids.append(offer.id)
        if request.user in offer.donor.ignore_list.all():
            exclude_offer_ids.append(offer.id)

        if offer.receive_help_from_who == MemberType.ALL:
            continue
        elif offer.receive_help_from_who == MemberType.VERIFIED_MEMBER:
            if not request.user.is_verified:
                exclude_offer_ids.append(offer.id)
        elif offer.receive_help_from_who == MemberType.FAVORITE:
            if not request.user.verified_favorites.filter(user=offer.donor).exists():
                exclude_offer_ids.append(offer.id)

        if offer.donor.id == request.user.id:
            if offer.id in exclude_offer_ids:
                exclude_offer_ids.remove(offer.id)

    offers = offers.exclude(id__in=exclude_offer_ids)
    return offers

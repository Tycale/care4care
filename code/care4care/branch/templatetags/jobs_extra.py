from django import template
register = template.Library()

@register.inclusion_tag('templatetags/offers.html')
def show_offers(request, offers, show_branch=True):
    return locals()

@register.inclusion_tag('templatetags/demands.html')
def show_demands(request, demands, show_branch=True, check_progress=True):
    return locals()
from django import template
register = template.Library()

@register.inclusion_tag('templatetags/offers.html')
def show_offers(request, offers):
    return locals()

@register.inclusion_tag('templatetags/demands.html')
def show_demands(request, demands):
    return locals()
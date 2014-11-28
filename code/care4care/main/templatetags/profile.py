from django import template
register = template.Library()

@register.inclusion_tag('templatetags/favorites.html')
def show_favorites(request, favorites, show_branch=True):
        return locals()

@register.inclusion_tag('templatetags/personal_network.html')
def show_personal_network(request, network, show_branch=True):
        return locals()

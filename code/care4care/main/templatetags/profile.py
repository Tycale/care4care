from django import template
register = template.Library()

@register.inclusion_tag('templatetags/favorites.html')
def show_favorites(request, favorites):
	return locals()

@register.inclusion_tag('templatetags/personal_network.html')
def show_personal_network(request, network):
	return locals()

@register.inclusion_tag('templatetags/ignored_list.html')
def show_ignore_list(request, ignore_list):
	return locals()


@register.inclusion_tag('templatetags/user_stats.html')
def show_user_stats(request, user_id):
	return locals()

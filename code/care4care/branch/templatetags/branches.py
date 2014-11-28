#-*- coding: utf-8 -*-
from django import template
from django.conf import settings

from branch.models import Branch

register = template.Library()

@register.inclusion_tag('templatetags/branches_admin.html', takes_context=True)
def branches(context):
	branches = Branch.objects.all()
	return locals()
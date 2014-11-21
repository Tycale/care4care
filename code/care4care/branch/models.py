from django.utils.translation import ugettext as _
from django.db import models

from main.models import User

class Branch(models.Model):
    name = models.CharField(verbose_name=_("Nom de la branche"), max_length=255)
    members = models.ManyToManyField(User, null=True, blank=True, through='', related_name="members", verbose_name=_("Membres de la branche"))

    class Meta:
        ordering = ['name']

class BranchMembers(models.Model):
	user = models.ForeignKey(User, related_name='membership')
    branch = models.ForeignKey(Branch, related_name='membership')
    is_admin = models.BooleanField(default=False)

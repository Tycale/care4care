from django.utils.translation import ugettext as _
from django.db import models

from main.models import User

class Branch(models.Model):
    name = models.CharField(verbose_name=_("Nom de la branche"), max_length=255)
    admins = models.ManyToManyField(User, null=True, blank=True, related_name="admins", verbose_name=_("Administrateurs de la branche"))
    members = models.ManyToManyField(User, null=True, blank=True, related_name="members", verbose_name=_("Membres de la branche"))
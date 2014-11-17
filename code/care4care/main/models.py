from django.utils.translation import ugettext as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from multiselectfield import MultiSelectField
from django.db import models
from django.core import validators
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.models import UserManager as BaseUserManager

import re

# TODO: complete
HOW_FOUND_CHOICES = (
    ('amis', _("Mes amis m'en ont parlés")),
    ('pubs', _("J'ai vu de la pub")),
    ('other', _("Autre")),
    )

COUNTRY_CHOICES = (
    ('be', _("Belgique")),
    ('fr', _("France")),
    ('nl', _("Pays-Bas")),
    ('lu', _("Luxembourg")),
    )

class CommonInfo(models.Model):
    """
    Common informations class
    """
    first_name = models.CharField(_('Prénom'), max_length=30, blank=False)
    last_name = models.CharField(_('Nom'), max_length=30, blank=False)
    location = models.CharField(_('Adresse'), max_length=256, null=True, blank=True)
    latitude = models.CharField(_('Latitude'), max_length=20, null=True, blank=True)
    longitude = models.CharField(_('Longitude'), max_length=20, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres."))
    phone_number = models.CharField(validators=[phone_regex], max_length=16, blank=True, verbose_name=_("Numéro de téléphone (fixe)"))
    mobile_number = models.CharField(validators=[phone_regex], max_length=16, blank=True, verbose_name=_("Numéro de téléphone mobile"))
    languages = MultiSelectField(choices=settings.LANGUAGES, verbose_name=_("Langues parlées"))

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        super_user = self._create_user(username, email, password, True, True, **extra_fields)
        super_user.languages = ['fr', 'be', 'nl']
        super_user.how_found = HOW_FOUND_CHOICES[0][0]
        super_user.save()
        return super_user

class User(AbstractBaseUser, PermissionsMixin, CommonInfo):
    """
    Custom user class
    """
    email = models.EmailField(_("Adresse email"), unique=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    username = models.CharField(_("Nom d'utilisateur"), max_length=30, unique=True,
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), _("Entrez un nom d'utilisateur valide.\
             30 caractères ou moins. Peut contenir des lettres, nombres et les caractères @/./+/-/_ "), 'invalid')
        ])
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    non_member = models.BooleanField(default=False)
    how_found = MultiSelectField(choices=HOW_FOUND_CHOICES, verbose_name=_("Comment avez-vous entendu parlé de Care4Care ?"))
    birth_date = models.DateField(blank=True, null=True, verbose_name=_("Date de naissance"))
    credit = models.IntegerField(default=0, verbose_name=_("Crédit restant")) # in minuts

    objects = UserManager()

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name',]
    USERNAME_FIELD = 'username'

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def __unicode__(self):
        return self.email


class Contact(CommonInfo):
    """
    Contact class
    """
    email = models.EmailField(_('Adresse email'), blank=True)
    relationship = models.CharField(max_length=255, blank=True, verbose_name=_("Votre relation par rapport à cette personne"))
    comments = models.CharField(max_length=255, blank=True, verbose_name=_("Commentaire supplémentaire"))

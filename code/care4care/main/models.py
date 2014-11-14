from django.utils.translation import ugettext as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from multiselectfield import MultiSelectField
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.models import UserManager

# TODO: complete
HOW_FOUND_CHOICES = (
    ('amis', _("Mes amis m'en ont parlés")),
    ('pubs', _("J'ai vu de la pub")),
    ('other', _("Autre")),
    )

CONTRY_CHOICES = (
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
    contry = models.CharField(choices=CONTRY_CHOICES, max_length=2, verbose_name=_("Pays"), default=CONTRY_CHOICES[0][0])
    address = models.CharField(max_length=255, verbose_name=_("Adresse postale"), blank=True)
    city = models.CharField(max_length=100, verbose_name=_("Ville"), blank=True)
    postal_code = models.IntegerField(max_length=10, verbose_name=_("Code postale"), blank=True, null=True)
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


class User(AbstractBaseUser, PermissionsMixin, CommonInfo):
    """
    Custom user class
    """
    email = models.EmailField('email address', unique=True, db_index=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    non_member = models.BooleanField(default=False)
    how_found = MultiSelectField(choices=HOW_FOUND_CHOICES, verbose_name=_("Comment avez-vous entendu parlé de Care4Care ?"))
    birth_date = models.DateField(blank=True, null=True, verbose_name=_("Date de naissance"))
    credit = models.IntegerField(default=0, verbose_name=_("Crédit restant")) # in minuts

    objects = UserManager()

    REQUIRED_FIELDS = ['username',]
    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return self.email

class Contact(CommonInfo):
    """
    Contact class
    """
    email = models.EmailField(_('Adresse email'), blank=True)
    relationship = models.CharField(max_length=255, blank=True, verbose_name=_("Votre relation par rapport à cette personne"))
    comments = models.CharField(max_length=255, blank=True, verbose_name=_("Commentaire supplémentaire"))








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

ACTIVE = 1
HOLIDAYS = 2
UNSUBSCRIBE = 3

STATUS = (
    (ACTIVE, _("Actif")),
    (HOLIDAYS, _("En vacance")),
    (UNSUBSCRIBE, _("Désactivé")),
    )

INBOX = 1
MAIL = 2

INFORMED_BY =(
    (INBOX, _("Boite à message")),
    (MAIL, _("Mail"))
    )

class MemberType():
    MEMBER = 1
    NON_MEMBER = 2
    VERIFIED_MEMBER = 3
    BRANCH_OFFICER = 4
    ALL = 5
    FAVORITE = 6

    MEMBER_TYPES = (
        (MEMBER, _("Membre")),
        (NON_MEMBER, _("Non-membre"))
        )

    MEMBER_TYPES_GROUP = (
        (ALL, _("Tous")),
        (VERIFIED_MEMBER, _("Membre vérifié")),
        (FAVORITE, _("Favoris (inclus le reseau personel)")),
        )

class JobCategory():
    visit_at_home = 1
    accompany_someone = 2
    transport_by_car = 3
    shopping = 4
    household = 5
    handyman_jobs = 6
    gardening_jobs = 7
    pets_care = 8
    personal_care = 9
    administration = 10
    other = 11
    special = 12

    JOB_CATEGORIES = ((
        (visit_at_home, _("Visite à la maison")),
        (accompany_someone, _("Tenir compagnie")),
        (transport_by_car, _("Transport par voiture")),
        (shopping, _("Shopping")),
        (household,_("Garder des maisons")),
        (handyman_jobs,_("Petit boulots manuels")),
        (gardening_jobs,_("Jardinage")),
        (pets_care,_("Garder des animaux")),
        (administration,_("Administratif")),
        (other,_("Autre")),
        (special,_("Special ... :D")),
        ))


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
    """
    https://github.com/django/django/blob/master/django/contrib/auth/models.py#L162
    """
    def create_superuser(self, username, email, password, **extra_fields):
        super_user = self._create_user(username, email, password, True, True, **extra_fields)
        super_user.languages = ['fr', 'be', 'nl']
        super_user.how_found = HOW_FOUND_CHOICES[0][0]
        super_user.user_type = MemberType.MEMBER

        super_user.save()
        return super_user

class User(AbstractBaseUser, PermissionsMixin, CommonInfo):
    """
    Custom user class
    AbstractBaseUser gives us the following fields :
        * password
        * last_login
        * is_active
    See https://github.com/django/django/blob/master/django/contrib/auth/models.py#L191
    PermissionsMixin gives us the following fields :
        * is_superuser
        * groups
        * user_permissions
    See https://github.com/django/django/blob/master/django/contrib/auth/models.py#L299
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

    status = models.IntegerField(choices=STATUS,
                                      default=ACTIVE)

    user_type = models.IntegerField(_("Type de compte"),choices=MemberType.MEMBER_TYPES,
                                      default=MemberType.MEMBER, help_text=_('Un member pourra aider ou être aidé alors qu\'un \
                                       non-membre est un professionnel qui s\'inscrira pour avoir accès aux données d\'un \
                                       passiant. Veuillez choisir celui qui vous correspond'))

    how_found = MultiSelectField(choices=HOW_FOUND_CHOICES, verbose_name=_("Comment avez-vous entendu parlé de Care4Care ?"))
    birth_date = models.DateField(blank=True, null=True, verbose_name=_("Date de naissance"))
    credit = models.IntegerField(default=0, verbose_name=_("Crédit restant")) # in minuts

    #Verified member
    # social_media = [] # Commented since we don't know how it'll be traited by the third-app.
    car = models.BooleanField(default=False)

    #non member
    organization = models.CharField(_("Organization"), max_length=100)
    work = models.CharField(_("Fonction"), max_length=100)

    # preference
    work_with = models.ManyToManyField('self')
    mail_preferences = models.IntegerField(choices=INFORMED_BY,
                                      default=INBOX, verbose_name=_("Recevoir mes messages par"))
    receive_help_from_who = models.IntegerField(choices=MemberType.MEMBER_TYPES_GROUP, default=MemberType.ALL,
    verbose_name=_("Recevoir des demandes et des offres de"))
    preferred_job = MultiSelectField(choices=JobCategory.JOB_CATEGORIES, verbose_name=_("Quels sont vos travaux préférés ?"))

    objects = UserManager()

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', ]
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

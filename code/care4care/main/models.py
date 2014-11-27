from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from multiselectfield import MultiSelectField
from django.db import models
from django.core import validators
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.models import UserManager as BaseUserManager
from django.core.urlresolvers import reverse

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
PRIORITY = (
    (1, _("A contacter en premier")),
    (2, _("A contacter")),
    (3, _("A contacter en dernier"))
    )

SCOOTER = 1
MOTO = 2
CAR = 3
TRUCK = 4
BUS = 5
TRACTOR = 6

DRIVER_LICENSE =(
    (SCOOTER, _('Vélomoteur')),
    (MOTO, _('Moto')),
    (CAR, _('Voiture')),
    (TRUCK, _('Camion')),
    (BUS, _('Bus')),
    (TRACTOR, _('Tracteur')),
    )

class MemberType:
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
        (FAVORITE, _("Favoris (inclus le réseau personnel)")),
        )

    VERBOSE_VM = _("Membre vérifié")
    VERBOSE_VNM = _("Non-membre vérifié")


class JobCategory:
    VISIT_AT_HOME = 1
    ACCOMPANY_SOMEONE = 2
    TRANSPORT_BY_CAR = 3
    SHOPPING = 4
    HOUSEHOULD = 5
    HANDYMAN_JOBS = 6
    GARDENING_JOBS = 7
    PETS_CARE = 8
    PERSONAL_CARE = 9
    ADMINISTRATION = 10
    OTHER = 11
    SPECIAL = 12

    JOB_CATEGORIES = ((
        (VISIT_AT_HOME, _("Visite à la maison")),
        (ACCOMPANY_SOMEONE, _("Tenir compagnie")),
        (TRANSPORT_BY_CAR, _("Transport par voiture")),
        (SHOPPING, _("Shopping")),
        (HOUSEHOULD, _("Garder des maisons")),
        (HANDYMAN_JOBS, _("Petits boulots manuels")),
        (GARDENING_JOBS, _("Jardinage")),
        (PETS_CARE, _("Garder des animaux")),
        (PERSONAL_CARE, _("Soins personnels")),
        (ADMINISTRATION, _("Administratif")),
        (OTHER, _("Autre")),
        (SPECIAL, _("Spécial ... :D")),
        ))

BOOL_CHOICES = ((True, _('Oui')), (False, _('Non')))

class VerifiedUser(models.Model):
    """
    Verified informations class
    """
    have_car = models.BooleanField(default=False, choices=BOOL_CHOICES, verbose_name=_("Disposez-vous d'une voiture ?"))
    can_wheelchair = models.BooleanField(default=False, choices=BOOL_CHOICES, verbose_name=_("Pouvez-vous transporter une chaise roulante dans votre voiture ?"))
    drive_license = MultiSelectField(choices=DRIVER_LICENSE, verbose_name=_("Type de permis de conduire"), blank=True)


    # preference
    work_with = models.ManyToManyField('User',related_name="verified_work_with", blank=True, null=True)

    # network management
    favorites = models.ManyToManyField('User',related_name="verified_favorites", blank=True, null=True)
    personal_network = models.ManyToManyField('User', verbose_name="Votre réseau personnel",related_name="verified_personal_network", blank=True, null=True)

    mail_preferences = models.IntegerField(choices=INFORMED_BY,
                                      default=INBOX, verbose_name=_("Recevoir mes messages par"))
    receive_help_from_who = models.IntegerField(choices=MemberType.MEMBER_TYPES_GROUP, default=MemberType.ALL,
                                      verbose_name=_("Recevoir des demandes et des offres de"))
    offered_job = MultiSelectField(choices=JobCategory.JOB_CATEGORIES, verbose_name=_("Quelles sont les tâches que vous souhaitez effectuer ?"), blank=True)
    asked_job = MultiSelectField(choices=JobCategory.JOB_CATEGORIES, verbose_name=_("Quelles sont les tâches dont vous avez besoin ?"), blank=True)

    # TODO : Schedule time

    facebook = models.URLField(verbose_name="Lien (URL) de votre profil Facebook", blank=True)

    hobbies = models.TextField(verbose_name=_("Vos hobbies"), blank=True)
    additional_info = models.TextField(verbose_name=_("Informations supplémentaires"), blank=True)


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
    languages = MultiSelectField(choices=settings.LANGUAGES, verbose_name=_("Langues parlées"), blank=True)

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    class Meta:
        abstract = True

class EmergencyContact(CommonInfo):
    user = models.ForeignKey('User', related_name="emergency_contacts")
    order = models.IntegerField(default=0, verbose_name=_("Ordre de priorité"), choices=PRIORITY)


class UserManager(BaseUserManager):
    """
    https://github.com/django/django/blob/master/django/contrib/auth/models.py#L162
    """
    def create_superuser(self, username, email, password, **extra_fields):
        super_user = self._create_user(username, email, password, True, True, **extra_fields)
        super_user.languages = ['fr', 'be', 'nl']
        super_user.how_found = HOW_FOUND_CHOICES[0][0]
        super_user.user_type = MemberType.MEMBER
        super_user.is_verified = True

        super_user.save()
        return super_user

class User(AbstractBaseUser, PermissionsMixin, CommonInfo, VerifiedUser):
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

    is_verified = models.BooleanField(default=False)

    status = models.IntegerField(choices=STATUS,
                                      default=ACTIVE)

    user_type = models.IntegerField(_("Type de compte"),choices=MemberType.MEMBER_TYPES,
                                      default=MemberType.MEMBER, help_text=_('Un member pourra aider ou être aidé alors qu\'un \
                                       non-membre est un professionnel qui s\'inscrira pour avoir accès aux données d\'un \
                                       patient. Veuillez choisir celui qui vous correspond'))

    how_found = MultiSelectField(choices=HOW_FOUND_CHOICES, verbose_name=_("Comment avez-vous entendu parler de Care4Care ?"))
    birth_date = models.DateField(blank=True, null=True, verbose_name=_("Date de naissance"))
    credit = models.IntegerField(default=0, verbose_name=_("Crédit restant")) # in minuts

    #Verified member
    # social_media = [] # Commented since we don't know how it'll be traited by the third-app.


    #non member
    organization = models.CharField(_("Organization"), max_length=100, blank=True)
    work = models.CharField(_("Fonction"), max_length=100, blank=True, null=True)

    objects = UserManager()

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', ]
    USERNAME_FIELD = 'username'

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def get_verbose_credit(self):
        credit = self.credit
        chunks = (
            (60 * 24 * 365, ('%d année', '%d années')), #Yeah.. We never know. Maybe slaves will use this app.
            (60 * 24 * 30, ('%d mois', '%d mois')),
            (60 * 24 * 7, ('%d semaine', '%d semaines')),
            (60 * 24, ('%d jour', '%d jours')),
            (60, ('%d heure', '%d heures')),
            (1, ('%d minute', '%d minutes'))
        )
        for i, (minuts, name) in enumerate(chunks):
                count = credit // minuts
                if count != 0:
                    break
        credit -= count * minuts
        if count > 2:
            result = (name[1] % count)
        else :
            result = (name[0] % count)
        while i + 1 < len(chunks):
            minuts2, name2 = chunks[i + 1]
            count2 = credit // minuts2
            if count2 != 0:
                if count2 > 2:
                    result += _(', ') + (name2[1] % count2)
                else :
                    result += _(', ') + (name2[0] % count2)
            credit -= count2 * minuts2
            i += 1
        return result

    def get_verbose_status(self):
         return STATUS[self.status-1][1]

    def get_account_type(self):
        if self.is_superuser :
            return _('superuser')
        if not self.is_verified :
            return MemberType.MEMBER_TYPES[self.user_type-1][1] + '<a href="' + reverse('verified_member_demand') + '"> <i class="fa fa-caret-square-o-up"></i></a>'
        else :
            if self.user_type == MemberType.MEMBER:
                return MemberType.VERBOSE_VM
            if self.user_type == MemberType.NON_MEMBER:
                return MemberType.VERBOSE_VNM
        return _('Inconnu')

    def __str__(self):
        return self.username

class Contact(CommonInfo):
    """
    Contact class
    """
    email = models.EmailField(_('Adresse email'), blank=True)
    relationship = models.CharField(max_length=255, blank=True, verbose_name=_("Votre relation par rapport à cette personne"))
    comments = models.CharField(max_length=255, blank=True, verbose_name=_("Commentaire supplémentaire"))


class VerifiedInformation(models.Model):
    """
    Doc for verfied member class
    """
    user = models.ForeignKey(User, null=True, blank=False)
    recomendation_letter_1 = models.FileField(upload_to='documents/', verbose_name=_("Lettre de recommendation n°1"), null=True, blank=False)
    recomendation_letter_2 = models.FileField(upload_to='documents/', verbose_name=_("Lettre de recommendation n°2"), null=True, blank=False)
    criminal_record = models.FileField(upload_to='documents/', verbose_name=_("Casier judiciaire"),null=True, blank=False)

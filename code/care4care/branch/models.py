from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.db import models

from multiselectfield import MultiSelectField

from main.models import User, JobCategory, MemberType

JOB_STATUS_CHOICES = (
    (1, _('créé')),
    (2, _('reçu proposition')),
    (3, _('proposition acceptée')),
    (4, _('completé')),
    (5, _('echoué')),
    )

TIME_CHOICES = (
    (1, _('Début de matinée (8h-10h)')),
    (2, _('Fin de matinée (10h-12h)')),
    (3, _('Midi (12h-13h)')),
    (4, _('Début d\'après-midi (13h-16h)')),
    (5, _('Fin d\'après-midi (16h-19h)')),
    (6, _('Repas du soir (19h-20h)')),
    (7, _('Début de soirée (20h-22h)')),
    (8, _('Fin de soirée (22h-00h)')),
    (9, _('Nuit (00h-8h)')),
    )

class Branch(models.Model):
    name = models.CharField(verbose_name=_("Nom de la branche"), max_length=255, help_text=_("Nom de la localité"))
    slug = models.SlugField()
    creator = models.ForeignKey(User, verbose_name=_("Créateur de la branche"))
    location = models.CharField(_('Adresse'), max_length=256, null=True, blank=True)
    latitude = models.CharField(_('Latitude'), max_length=20, null=True, blank=True)
    longitude = models.CharField(_('Longitude'), max_length=20, null=True, blank=True)
    members = models.ManyToManyField(User, null=True, blank=True, through='BranchMembers', related_name="members", verbose_name=_("Membres de la branche"))

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Branch, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('branch_home', (), {'slug' : self.slug, 'id' : self.id})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class BranchMembers(models.Model):
    user = models.ForeignKey(User, related_name='membership')
    branch = models.ForeignKey(Branch, related_name='membership')
    is_admin = models.BooleanField(default=False)
    joined = models.DateTimeField(verbose_name=_("date d'arrivé"))

    class Meta:
        ordering = ['is_admin']

class Job(models.Model):
    branch = models.ForeignKey(Branch, verbose_name=_("Branche"), related_name="branch")
    donor = models.ForeignKey(User, verbose_name=_("Donneur"), related_name="donor", null=True)
    receiver =  models.ForeignKey(User, verbose_name=_("Receveur"), related_name="receiver", null=True)
    title = models.CharField(_('Titre'), max_length=120, null=True, blank=False)
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    estimated_time = models.IntegerField(verbose_name=_("Temps estimé (en minutes)"))
    real_time = models.IntegerField(verbose_name=_("Temps réel (en minutes)"), blank=True, null=True)
    category = models.IntegerField(choices=JobCategory.JOB_CATEGORIES, verbose_name=_("Type d'aide"))
    receive_help_from_who = models.IntegerField(choices=MemberType.MEMBER_TYPES_GROUP, default=MemberType.ALL,
                                      verbose_name=_("Qui peut voir et répondre à la demande/offre ?"))
    date = models.DateTimeField(verbose_name=_("Date"))
    time = MultiSelectField(choices=TIME_CHOICES, verbose_name=_("Heure(s) possible(s)"), blank=False, help_text=_('Selectionnez les heures qui vous conviennent'))
    km = models.IntegerField(verbose_name=_("km"), blank=True, null=True)
    location = models.CharField(_('Adresse'), max_length=256, null=True, blank=True)
    latitude = models.CharField(_('Latitude'), max_length=20, null=True, blank=True)
    longitude = models.CharField(_('Longitude'), max_length=20, null=True, blank=True)

    state = models.IntegerField(choices=JOB_STATUS_CHOICES, default=1,
                                      verbose_name=_("Status"))
    is_offer= models.BooleanField(default=False,verbose_name=_("Est-ce une offre ?"))

    def get_verbose_category(self):
        return JobCategory.JOB_CATEGORIES[self.category-1][1]

    def get_verbose_status(self):
        return JOB_STATUS_CHOICES[self.state-1][1]

class Comment(models.Model):
    user = models.ForeignKey(User)
    job = models.ForeignKey(Job)
    comment = models.TextField(verbose_name=_("Commentaire"))

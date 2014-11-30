from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from multiselectfield import MultiSelectField

from main.models import User, JobCategory, MemberType

JOB_STATUS_CHOICES = (
    (1, _('créé')),
    (2, _('reçu proposition')),
    (3, _('proposition acceptée')),
    (4, _('completé')),
    (5, _('échoué')),
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

SHORT_TIME = (
    _('8h-10h'),
    _('10h-12h'),
    _('12h-13h'),
    _('13h-16h'),
    _('16h-19h'),
    _('19h-20h'),
    _('20h-22h'),
    _('22h-00h'),
    _('00h-8h'),
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
        return ('branch_home', (), {'slug' : self.slug, 'branch_id' : self.id})

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
        ordering = ['-is_admin']

class Comment(models.Model):
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    comment = models.TextField(verbose_name=_("Commentez"))
    date = models.DateTimeField(verbose_name=_("Date"), auto_now=True)

    def __str__(self):
        return '{} {} {}'.format(self.user, self.date, self.content_object)

    class Meta:
        ordering = ['date']

class Job(models.Model):
    branch = models.ForeignKey(Branch, verbose_name=_("Branche"), related_name="%(class)s_branch")
    donor = models.ForeignKey(User, verbose_name=_("Donneur"), related_name="%(class)s_donor", null=True)
    receiver =  models.ForeignKey(User, verbose_name=_("Receveur"), related_name="%(class)s_receiver", null=True)
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    category = MultiSelectField(choices=JobCategory.JOB_CATEGORIES, verbose_name=_("Type d'aide"))
    receive_help_from_who = models.IntegerField(choices=MemberType.MEMBER_TYPES_GROUP, default=MemberType.ALL,
                                      verbose_name=_("Qui peut voir et répondre à la demande/offre ?"))
    date = models.DateTimeField(verbose_name=_("Date"))
    time = MultiSelectField(choices=TIME_CHOICES, verbose_name=_("Heures de disponibilité"), blank=False, help_text=_('Selectionnez les heures qui vous conviennent'))

    def get_verbose_category(self):
        if not self.category:
            return ''
        return ', '.join([str(l[1]) for l in JobCategory.JOB_CATEGORIES if (str(l[0]) in self.category)])

    def get_verbose_time(self):
        if not self.time:
            return ''
        return ', '.join([str(l[1]) for l in TIME_CHOICES if (str(l[0]) in self.time)])

    def get_short_time(self):
        if not self.time:
            return ''
        return ', '.join([str(SHORT_TIME[l[0]-1]) for l in TIME_CHOICES if (str(l[0]) in self.time)])

    class Meta:
        abstract = True

class Demand(Job):
    title = models.CharField(_('Titre'), max_length=120, null=True, blank=False)
    location = models.CharField(_('Adresse'), max_length=256, null=True, blank=True)
    latitude = models.CharField(_('Latitude'), max_length=20, null=True, blank=True)
    longitude = models.CharField(_('Longitude'), max_length=20, null=True, blank=True)
    estimated_time = models.IntegerField(verbose_name=_("Temps estimé (en minutes)"), blank=True, null=True)
    real_time = models.IntegerField(verbose_name=_("Temps réel (en minutes)"), blank=True, null=True)
    comments = GenericRelation(Comment)

    @models.permalink
    def get_absolute_url(self):
        return ('see_demand', (), {'branch_id': self.branch.id, 'slug': self.branch.slug, 'demand_id': self.id})

    def __str__(self):
        return '{} - {} - {}'.format(self.title, self.receiver, self.branch)

class Offer(Job):
    comments = GenericRelation(Comment)

    @models.permalink
    def get_absolute_url(self):
        return ('see_offer', (), {'branch_id': self.branch.id, 'slug': self.branch.slug, 'offer_id': self.id})
    def __str__(self):
        return '{} - {}'.format(self.donor, self.branch)




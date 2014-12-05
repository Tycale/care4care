from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManager

from multiselectfield import MultiSelectField
from django.utils import timezone
from main.models import User, JobCategory, MemberType

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
    """ Representation of a branch """
    name = models.CharField(verbose_name=_("Nom de la branche"), max_length=255)
    slug = models.SlugField()
    creator = models.ForeignKey(User, verbose_name=_("Créateur de la branche"))
    location = models.CharField(_('Adresse'), max_length=256, null=True, blank=True)
    latitude = models.CharField(_('Latitude'), max_length=20, null=True, blank=True)
    longitude = models.CharField(_('Longitude'), max_length=20, null=True, blank=True)
    members = models.ManyToManyField(User, null=True, blank=True, through='BranchMembers', related_name="members", verbose_name=_("Membres de la branche"))
    banned = models.ManyToManyField(User, null=True, blank=True, related_name="banned_users", verbose_name=_("Membres bannis"))

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
    """ Class used for the representation of a member who is in a branch """
    user = models.ForeignKey(User, related_name='membership')
    branch = models.ForeignKey(Branch, related_name='membership')
    is_admin = models.BooleanField(default=False)
    joined = models.DateTimeField(verbose_name=_("date d'arrivé"))

    def __str__(self):
        res = '{} in {}'.format(self.user, self.branch)
        if self.is_admin:
            res += ' [admin]'
        return res

    class Meta:
        ordering = ['-is_admin']

class Comment(models.Model):
    """ Representation of a comment """
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

class JobManager(QuerySet):
    def up_to_date(self):
        date_now = timezone.now() + timezone.timedelta(hours=-24)
        return self.filter(date__gte=date_now)

    def down_to_date(self):
        date_now = timezone.now() + timezone.timedelta(hours=24)
        return self.filter(date__lte=date_now)

    def no_successs(self):
        return self.filter(success_fill=False)


class Job(models.Model):
    """ Representation of a job (demand or offer) """
    branch = models.ForeignKey(Branch, verbose_name=_("Branche"), related_name="%(class)s_branch")
    donor = models.ForeignKey(User, verbose_name=_("Donneur"), related_name="%(class)s_donor", null=True, blank=True)
    receiver =  models.ForeignKey(User, verbose_name=_("Receveur"), related_name="%(class)s_receiver", null=True, blank=True)
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

    objects = PassThroughManager.for_queryset_class(JobManager)()

    class Meta:
        abstract = True

class Demand(Job):
    """ Representation of a demand """
    title = models.CharField(_('Titre'), max_length=120, null=True, blank=False)
    location = models.CharField(_('Adresse'), max_length=256, null=True, blank=True)
    latitude = models.CharField(_('Latitude'), max_length=20, null=True, blank=True)
    longitude = models.CharField(_('Longitude'), max_length=20, null=True, blank=True)
    estimated_time = models.IntegerField(verbose_name=_("Temps estimé (en minutes)"), blank=True, null=True)
    real_time = models.IntegerField(verbose_name=_("Temps réel (en minutes)"), blank=True, null=True)
    comments = GenericRelation(Comment)
    volunteers = models.ManyToManyField(User, null=True, blank=True, through='DemandProposition', related_name="volunteers", verbose_name=_("Propositions"))
    closed = models.BooleanField(verbose_name=_("Vontaire assigné"), default=False)
    success_fill = models.BooleanField(verbose_name=_("Demande de confirmation envoyée"), default=False)
    km = models.IntegerField(verbose_name=_("Distance depuis domicile"), blank=True, null=True)
    success = models.NullBooleanField(verbose_name=_("Tâche finie avec succès"), null=True, blank=True, default=None)

    @models.permalink
    def get_absolute_url(self):
        return ('see_demand', (), {'branch_id': self.branch.id, 'slug': self.branch.slug, 'demand_id': self.id})

    def __str__(self):
        return '{} - {} - {}'.format(self.title, self.receiver, self.branch)

    class Meta:
        ordering = ['date']

class Offer(Job):
    """ Representation of a job """
    comments = GenericRelation(Comment)

    @models.permalink
    def get_absolute_url(self):
        return ('see_offer', (), {'branch_id': self.branch.id, 'slug': self.branch.slug, 'offer_id': self.id})
    def __str__(self):
        return '{} - {}'.format(self.donor, self.branch)

    class Meta:
        ordering = ['date']

class DemandPropositionManager(QuerySet):
    def up_to_date(self):
        date_now = timezone.now() + timezone.timedelta(hours=-24)
        return self.filter(demand__date__gte=date_now)

    def down_to_date(self):
        date_now = timezone.now() + timezone.timedelta(hours=24)
        return self.filter(demand__date__lte=date_now)

    def no_successs(self):
        return self.filter(demand__success_fill=False)

class DemandProposition(models.Model):
    """ Representation of a demand Proposition"""
    user = models.ForeignKey(User, related_name='uservol')
    demand = models.ForeignKey(Demand, related_name='propositions')
    comment = models.TextField(verbose_name=_("Commentaire (facultatif)"), blank=True, null=True)
    created = models.DateTimeField(verbose_name=_("Date de création"), auto_now=True)
    accepted = models.BooleanField(verbose_name=_("Proposition acceptée"), default=False)
    km = models.IntegerField(verbose_name=_("Distance depuis domicile"), blank=True, null=True)
    time = MultiSelectField(choices=TIME_CHOICES, verbose_name=_("Heure(s) choisie(s)"), blank=False, help_text=_('Selectionnez les heures qui vous conviennent'))

    objects = PassThroughManager.for_queryset_class(DemandPropositionManager)()

    def get_verbose_time(self):
        if not self.time:
            return ''
        return ', '.join([str(l[1]) for l in TIME_CHOICES if (str(l[0]) in self.time)])

    class Meta:
        ordering = ['-created']


class SuccessDemand(models.Model):
    """ Representation of a complete demand"""
    demand = models.ForeignKey(Demand, related_name='success_demand', blank=True, null=True)
    comment = models.TextField(verbose_name=_('Commentaire'), blank=True, null=True)
    time = models.IntegerField(verbose_name=_("Temps passé (en minutes)"), blank=True, null=True)
    ask_to = models.ForeignKey(User, related_name='success_pending', blank=True, null=True)
    asked_by = models.ForeignKey(User, related_name='approval_pending', blank=True, null=True)
    branch = models.ForeignKey(Branch, related_name='success_branch_pending', blank=True, null=True)
    created = models.DateTimeField(verbose_name=_("Date de création"), auto_now=True)

    class Meta:
        ordering = ['-created']


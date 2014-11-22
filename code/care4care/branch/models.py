from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
from django.db import models

from main.models import User, JobCategory

class Branch(models.Model):
    name = models.CharField(verbose_name=_("Nom de la branche"), max_length=255)
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

    class Meta:
        ordering = ['name']

class BranchMembers(models.Model):
    user = models.ForeignKey(User, related_name='membership')
    branch = models.ForeignKey(Branch, related_name='membership')
    is_admin = models.BooleanField(default=False)
    joined = models.DateTimeField(verbose_name=_("date d'arrivé"))

class Job(models.Model):
    branch = models.ForeignKey(Branch, verbose_name=_("Branche"), related_name="branch") 
    donor = models.ForeignKey(User, verbose_name=_("Donneur"), related_name="donor")
    receiver =  models.ForeignKey(User, verbose_name=_("Receveur"), related_name="receiver")
    description = models.TextField(verbose_name=_("Description"))
    estimated_time = models.IntegerField(verbose_name=_("Temps estimé"))
    real_time = models.IntegerField(verbose_name=_("Temps réel"))
    category = models.IntegerField(choices=JobCategory.JOB_CATEGORIES, verbose_name=_("Type d'aide"))
    date = models.DateTimeField(verbose_name=_("Date de l'aide"))
    km = models.IntegerField(verbose_name=_("km"))
    location = models.CharField(_('Adresse'), max_length=256, null=True, blank=True)
    latitude = models.CharField(_('Latitude'), max_length=20, null=True, blank=True)
    longitude = models.CharField(_('Longitude'), max_length=20, null=True, blank=True)

class Comment(models.Model):
    user = models.ForeignKey(User)
    job = models.ForeignKey(Job)
    comment = models.TextField(verbose_name=_("Commentaire"))

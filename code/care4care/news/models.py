from django.db import models
from main.models import User
from django.template.defaultfilters import slugify



# Create your models here.
class News(models.Model):
    titre = models.CharField(max_length=250, null=False, blank=False, verbose_name=u"Titre de l'article")
    slug = models.SlugField()
    corps = models.TextField(u"Corps de l'article")
    date_creation = models.DateTimeField(auto_now_add=True, editable=False)
    date_debut = models.DateTimeField(u"Date de publication désirée")
    date_fin = models.DateTimeField(u"Date de fin de publication (laisser vide si aucune expiration voulue)", blank=True, null=True)
    auteur = models.ForeignKey(User, blank=True, null=True)
    
    visible = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.titre)
        super(News, self).save(*args, **kwargs)

    def __str__(self):
        return self.titre

    @models.permalink
    def get_absolute_url(self):
        return ('news_read', (), { 'id' : self.id, 'slug' : self.slug,})

    @models.permalink
    def get_absolute_modify_url(self):
        return ('news_modify', (), { 'id' : self.id, 'slug' : self.slug,})

    class Meta:
        ordering = ['-date_debut'] 
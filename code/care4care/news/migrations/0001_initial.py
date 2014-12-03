# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('titre', models.CharField(max_length=250, verbose_name="Titre de l'article")),
                ('slug', models.SlugField()),
                ('corps', models.TextField(verbose_name="Corps de l'article")),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_debut', models.DateTimeField(verbose_name='Date de publication désirée')),
                ('date_fin', models.DateTimeField(blank=True, verbose_name='Date de fin de publication (laisser vide si aucune expiration voulue)', null=True)),
                ('visible', models.BooleanField(default=False)),
                ('auteur', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

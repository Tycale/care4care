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
            name='Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='Nom de la branche', max_length=255, help_text='Nom de la localité')),
                ('slug', models.SlugField()),
                ('location', models.CharField(verbose_name='Adresse', max_length=256, blank=True, null=True)),
                ('latitude', models.CharField(verbose_name='Latitude', max_length=20, blank=True, null=True)),
                ('longitude', models.CharField(verbose_name='Longitude', max_length=20, blank=True, null=True)),
                ('creator', models.ForeignKey(verbose_name='Créateur de la branche', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BranchMembers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('joined', models.DateTimeField(verbose_name="date d'arrivé")),
                ('branch', models.ForeignKey(related_name='membership', to='branch.Branch')),
                ('user', models.ForeignKey(related_name='membership', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['is_admin'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('comment', models.TextField(verbose_name='Commentaire')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='Titre', max_length=120, null=True)),
                ('description', models.TextField(verbose_name='Description')),
                ('estimated_time', models.IntegerField(verbose_name='Temps estimé')),
                ('real_time', models.IntegerField(verbose_name='Temps réel')),
                ('category', models.IntegerField(verbose_name="Type d'aide", choices=[(1, 'Visite à la maison'), (2, 'Tenir compagnie'), (3, 'Transport par voiture'), (4, 'Shopping'), (5, 'Garder des maisons'), (6, 'Petits boulots manuels'), (7, 'Jardinage'), (8, 'Garder des animaux'), (9, 'Soins personnels'), (10, 'Administratif'), (11, 'Autre'), (12, 'Spécial ... :D')])),
                ('date', models.DateTimeField(verbose_name="Date de l'aide")),
                ('km', models.IntegerField(verbose_name='km')),
                ('location', models.CharField(verbose_name='Adresse', max_length=256, blank=True, null=True)),
                ('latitude', models.CharField(verbose_name='Latitude', max_length=20, blank=True, null=True)),
                ('longitude', models.CharField(verbose_name='Longitude', max_length=20, blank=True, null=True)),
                ('branch', models.ForeignKey(verbose_name='Branche', related_name='branch', to='branch.Branch')),
                ('donor', models.ForeignKey(verbose_name='Donneur', related_name='donor', to=settings.AUTH_USER_MODEL, null=True)),
                ('receiver', models.ForeignKey(verbose_name='Receveur', related_name='receiver', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='comment',
            name='job',
            field=models.ForeignKey(to='branch.Job'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='branch',
            name='members',
            field=models.ManyToManyField(verbose_name='Membres de la branche', blank=True, through='branch.BranchMembers', related_name='members', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('branch', '0011_auto_20141129_2334'),
    ]

    operations = [
        migrations.CreateModel(
            name='Demand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('category', multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Visite à la maison'), (2, 'Tenir compagnie'), (3, 'Transport par voiture'), (4, 'Shopping'), (5, 'Garder des maisons'), (6, 'Petits boulots manuels'), (7, 'Jardinage'), (8, 'Garder des animaux'), (9, 'Soins personnels'), (10, 'Administratif'), (11, 'Autre'), (12, 'Spécial ... :D')], max_length=26, verbose_name="Type d'aide")),
                ('receive_help_from_who', models.IntegerField(default=5, choices=[(5, 'Tous'), (3, 'Membre vérifié'), (6, 'Favoris (inclus le réseau personnel)')], verbose_name='Qui peut voir et répondre à la demande/offre ?')),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('time', multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Début de matinée (8h-10h)'), (2, 'Fin de matinée (10h-12h)'), (3, 'Midi (12h-13h)'), (4, "Début d'après-midi (13h-16h)"), (5, "Fin d'après-midi (16h-19h)"), (6, 'Repas du soir (19h-20h)'), (7, 'Début de soirée (20h-22h)'), (8, 'Fin de soirée (22h-00h)'), (9, 'Nuit (00h-8h)')], max_length=17, help_text='Selectionnez les heures qui vous conviennent', verbose_name='Heure(s) possible(s)')),
                ('title', models.CharField(max_length=120, null=True, verbose_name='Titre')),
                ('location', models.CharField(blank=True, max_length=256, null=True, verbose_name='Adresse')),
                ('latitude', models.CharField(blank=True, max_length=20, null=True, verbose_name='Latitude')),
                ('longitude', models.CharField(blank=True, max_length=20, null=True, verbose_name='Longitude')),
                ('estimated_time', models.IntegerField(blank=True, null=True, verbose_name='Temps estimé (en minutes)')),
                ('real_time', models.IntegerField(blank=True, null=True, verbose_name='Temps réel (en minutes)')),
                ('branch', models.ForeignKey(related_name='demand_branch', to='branch.Branch', verbose_name='Branche')),
                ('donor', models.ForeignKey(related_name='demand_donor', to=settings.AUTH_USER_MODEL, null=True, verbose_name='Donneur')),
                ('receiver', models.ForeignKey(related_name='demand_receiver', to=settings.AUTH_USER_MODEL, null=True, verbose_name='Receveur')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('category', multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Visite à la maison'), (2, 'Tenir compagnie'), (3, 'Transport par voiture'), (4, 'Shopping'), (5, 'Garder des maisons'), (6, 'Petits boulots manuels'), (7, 'Jardinage'), (8, 'Garder des animaux'), (9, 'Soins personnels'), (10, 'Administratif'), (11, 'Autre'), (12, 'Spécial ... :D')], max_length=26, verbose_name="Type d'aide")),
                ('receive_help_from_who', models.IntegerField(default=5, choices=[(5, 'Tous'), (3, 'Membre vérifié'), (6, 'Favoris (inclus le réseau personnel)')], verbose_name='Qui peut voir et répondre à la demande/offre ?')),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('time', multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Début de matinée (8h-10h)'), (2, 'Fin de matinée (10h-12h)'), (3, 'Midi (12h-13h)'), (4, "Début d'après-midi (13h-16h)"), (5, "Fin d'après-midi (16h-19h)"), (6, 'Repas du soir (19h-20h)'), (7, 'Début de soirée (20h-22h)'), (8, 'Fin de soirée (22h-00h)'), (9, 'Nuit (00h-8h)')], max_length=17, help_text='Selectionnez les heures qui vous conviennent', verbose_name='Heure(s) possible(s)')),
                ('branch', models.ForeignKey(related_name='offer_branch', to='branch.Branch', verbose_name='Branche')),
                ('donor', models.ForeignKey(related_name='offer_donor', to=settings.AUTH_USER_MODEL, null=True, verbose_name='Donneur')),
                ('receiver', models.ForeignKey(related_name='offer_receiver', to=settings.AUTH_USER_MODEL, null=True, verbose_name='Receveur')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='job',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='job',
            name='donor',
        ),
        migrations.RemoveField(
            model_name='job',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='job',
        ),
        migrations.DeleteModel(
            name='Job',
        ),
        migrations.AddField(
            model_name='comment',
            name='content_type',
            field=models.ForeignKey(default=0, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='object_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]

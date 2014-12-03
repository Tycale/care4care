# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0029_auto_20141203_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='creator',
            field=models.ForeignKey(verbose_name='Créateur de la branche', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='location',
            field=models.CharField(verbose_name='Adresse', max_length=256, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='members',
            field=models.ManyToManyField(related_name='members', to=settings.AUTH_USER_MODEL, through='branch.BranchMembers', verbose_name='Membres de la branche', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(verbose_name='Nom de la branche', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branchmembers',
            name='joined',
            field=models.DateTimeField(verbose_name="date d'arrivé"),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(verbose_name='Commentez'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='branch',
            field=models.ForeignKey(related_name='demand_branch', to='branch.Branch', verbose_name='Branche'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name="Type d'aide", max_length=21, choices=[('1', 'Visite à la maison'), ('2', 'Tenir compagnie'), ('3', 'Transport par voiture'), ('4', 'Shopping'), ('5', 'Garder des maisons'), ('6', 'Petits boulots manuels'), ('7', 'Jardinage'), ('8', 'Garder des animaux'), ('9', 'Soins personnels'), ('a', 'Administratif'), ('b', 'Autre')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='closed',
            field=models.BooleanField(verbose_name='Vontaire assigné', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='donor',
            field=models.ForeignKey(verbose_name='Donneur', to=settings.AUTH_USER_MODEL, related_name='demand_donor', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='estimated_time',
            field=models.IntegerField(verbose_name='Temps estimé (en minutes)', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='km',
            field=models.IntegerField(verbose_name='Distance depuis domicile', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='location',
            field=models.CharField(verbose_name='Adresse', max_length=256, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='real_time',
            field=models.IntegerField(verbose_name='Temps réel (en minutes)', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='receive_help_from_who',
            field=models.IntegerField(verbose_name='Qui peut voir et répondre à la demande/offre ?', default=5, choices=[(5, 'Tous'), (3, 'Membre vérifié'), (6, 'Mes membres favoris')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='receiver',
            field=models.ForeignKey(verbose_name='Receveur', to=settings.AUTH_USER_MODEL, related_name='demand_receiver', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='time',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Heures de disponibilité', max_length=17, help_text='Selectionnez les heures qui vous conviennent', choices=[(1, 'Début de matinée (8h-10h)'), (2, 'Fin de matinée (10h-12h)'), (3, 'Midi (12h-13h)'), (4, "Début d'après-midi (13h-16h)"), (5, "Fin d'après-midi (16h-19h)"), (6, 'Repas du soir (19h-20h)'), (7, 'Début de soirée (20h-22h)'), (8, 'Fin de soirée (22h-00h)'), (9, 'Nuit (00h-8h)')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='title',
            field=models.CharField(verbose_name='Titre', max_length=120, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demandproposition',
            name='accepted',
            field=models.BooleanField(verbose_name='Proposition acceptée', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demandproposition',
            name='comment',
            field=models.TextField(verbose_name='Commentaire (facultatif)', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demandproposition',
            name='km',
            field=models.IntegerField(verbose_name='Distance depuis domicile', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demandproposition',
            name='time',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Heure(s) choisie(s)', max_length=17, help_text='Selectionnez les heures qui vous conviennent', choices=[(1, 'Début de matinée (8h-10h)'), (2, 'Fin de matinée (10h-12h)'), (3, 'Midi (12h-13h)'), (4, "Début d'après-midi (13h-16h)"), (5, "Fin d'après-midi (16h-19h)"), (6, 'Repas du soir (19h-20h)'), (7, 'Début de soirée (20h-22h)'), (8, 'Fin de soirée (22h-00h)'), (9, 'Nuit (00h-8h)')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='branch',
            field=models.ForeignKey(related_name='offer_branch', to='branch.Branch', verbose_name='Branche'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name="Type d'aide", max_length=21, choices=[('1', 'Visite à la maison'), ('2', 'Tenir compagnie'), ('3', 'Transport par voiture'), ('4', 'Shopping'), ('5', 'Garder des maisons'), ('6', 'Petits boulots manuels'), ('7', 'Jardinage'), ('8', 'Garder des animaux'), ('9', 'Soins personnels'), ('a', 'Administratif'), ('b', 'Autre')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='donor',
            field=models.ForeignKey(verbose_name='Donneur', to=settings.AUTH_USER_MODEL, related_name='offer_donor', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='receive_help_from_who',
            field=models.IntegerField(verbose_name='Qui peut voir et répondre à la demande/offre ?', default=5, choices=[(5, 'Tous'), (3, 'Membre vérifié'), (6, 'Mes membres favoris')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='receiver',
            field=models.ForeignKey(verbose_name='Receveur', to=settings.AUTH_USER_MODEL, related_name='offer_receiver', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='time',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Heures de disponibilité', max_length=17, help_text='Selectionnez les heures qui vous conviennent', choices=[(1, 'Début de matinée (8h-10h)'), (2, 'Fin de matinée (10h-12h)'), (3, 'Midi (12h-13h)'), (4, "Début d'après-midi (13h-16h)"), (5, "Fin d'après-midi (16h-19h)"), (6, 'Repas du soir (19h-20h)'), (7, 'Début de soirée (20h-22h)'), (8, 'Fin de soirée (22h-00h)'), (9, 'Nuit (00h-8h)')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='successdemand',
            name='comment',
            field=models.TextField(verbose_name='Commentaire'),
            preserve_default=True,
        ),
    ]

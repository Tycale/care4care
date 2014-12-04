# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import multiselectfield.db.fields
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    replaces = [('branch', '0001_initial'), ('branch', '0002_auto_20141127_0251'), ('branch', '0003_auto_20141127_0309'), ('branch', '0004_auto_20141127_0310'), ('branch', '0005_auto_20141129_1015'), ('branch', '0005_auto_20141129_0939'), ('branch', '0006_merge'), ('branch', '0007_job_receive_help_from_who'), ('branch', '0008_job_state'), ('branch', '0009_job_is_offer'), ('branch', '0010_auto_20141129_2113'), ('branch', '0011_auto_20141129_2334'), ('branch', '0012_auto_20141130_0042'), ('branch', '0013_auto_20141130_0402'), ('branch', '0014_auto_20141130_0440'), ('branch', '0015_auto_20141130_1904'), ('branch', '0016_auto_20141130_1948'), ('branch', '0017_auto_20141130_2043'), ('branch', '0018_auto_20141201_0017'), ('branch', '0019_auto_20141201_1201'), ('branch', '0020_auto_20141201_2102')]

    dependencies = [
        ('contenttypes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(verbose_name='Nom de la branche', max_length=255, help_text='Nom de la localité')),
                ('slug', models.SlugField()),
                ('location', models.CharField(null=True, verbose_name='Adresse', max_length=256, blank=True)),
                ('latitude', models.CharField(null=True, verbose_name='Latitude', max_length=20, blank=True)),
                ('longitude', models.CharField(null=True, verbose_name='Longitude', max_length=20, blank=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('comment', models.TextField(verbose_name='Commentaire')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('content_type', models.ForeignKey(default=0, to='contenttypes.ContentType')),
                ('object_id', models.PositiveIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='branch',
            name='members',
            field=models.ManyToManyField(null=True, verbose_name='Membres de la branche', through='branch.BranchMembers', related_name='members', blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Demand',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('category', multiselectfield.db.fields.MultiSelectField(verbose_name="Type d'aide", max_length=26, choices=[(1, 'Visite à la maison'), (2, 'Tenir compagnie'), (3, 'Transport par voiture'), (4, 'Shopping'), (5, 'Garder des maisons'), (6, 'Petits boulots manuels'), (7, 'Jardinage'), (8, 'Garder des animaux'), (9, 'Soins personnels'), (10, 'Administratif'), (11, 'Autre'), (12, 'Spécial ... :D')])),
                ('receive_help_from_who', models.IntegerField(verbose_name='Qui peut voir et répondre à la demande/offre ?', choices=[(5, 'Tous'), (3, 'Membre vérifié'), (6, 'Favoris (inclus le réseau personnel)')], default=5)),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('time', multiselectfield.db.fields.MultiSelectField(verbose_name='Heures de disponibilité', max_length=17, choices=[(1, 'Début de matinée (8h-10h)'), (2, 'Fin de matinée (10h-12h)'), (3, 'Midi (12h-13h)'), (4, "Début d'après-midi (13h-16h)"), (5, "Fin d'après-midi (16h-19h)"), (6, 'Repas du soir (19h-20h)'), (7, 'Début de soirée (20h-22h)'), (8, 'Fin de soirée (22h-00h)'), (9, 'Nuit (00h-8h)')], help_text='Selectionnez les heures qui vous conviennent')),
                ('title', models.CharField(null=True, verbose_name='Titre', max_length=120)),
                ('location', models.CharField(null=True, verbose_name='Adresse', max_length=256, blank=True)),
                ('latitude', models.CharField(null=True, verbose_name='Latitude', max_length=20, blank=True)),
                ('longitude', models.CharField(null=True, verbose_name='Longitude', max_length=20, blank=True)),
                ('estimated_time', models.IntegerField(null=True, verbose_name='Temps estimé (en minutes)', blank=True)),
                ('real_time', models.IntegerField(null=True, verbose_name='Temps réel (en minutes)', blank=True)),
                ('branch', models.ForeignKey(verbose_name='Branche', related_name='demand_branch', to='branch.Branch')),
                ('donor', models.ForeignKey(null=True, verbose_name='Donneur', related_name='demand_donor', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(null=True, verbose_name='Receveur', related_name='demand_receiver', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('category', multiselectfield.db.fields.MultiSelectField(verbose_name="Type d'aide", max_length=26, choices=[(1, 'Visite à la maison'), (2, 'Tenir compagnie'), (3, 'Transport par voiture'), (4, 'Shopping'), (5, 'Garder des maisons'), (6, 'Petits boulots manuels'), (7, 'Jardinage'), (8, 'Garder des animaux'), (9, 'Soins personnels'), (10, 'Administratif'), (11, 'Autre'), (12, 'Spécial ... :D')])),
                ('receive_help_from_who', models.IntegerField(verbose_name='Qui peut voir et répondre à la demande/offre ?', choices=[(5, 'Tous'), (3, 'Membre vérifié'), (6, 'Favoris (inclus le réseau personnel)')], default=5)),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('time', multiselectfield.db.fields.MultiSelectField(verbose_name='Heures de disponibilité', max_length=17, choices=[(1, 'Début de matinée (8h-10h)'), (2, 'Fin de matinée (10h-12h)'), (3, 'Midi (12h-13h)'), (4, "Début d'après-midi (13h-16h)"), (5, "Fin d'après-midi (16h-19h)"), (6, 'Repas du soir (19h-20h)'), (7, 'Début de soirée (20h-22h)'), (8, 'Fin de soirée (22h-00h)'), (9, 'Nuit (00h-8h)')], help_text='Selectionnez les heures qui vous conviennent')),
                ('branch', models.ForeignKey(verbose_name='Branche', related_name='offer_branch', to='branch.Branch')),
                ('donor', models.ForeignKey(null=True, verbose_name='Donneur', related_name='offer_donor', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(null=True, verbose_name='Receveur', related_name='offer_receiver', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['date']},
        ),
        migrations.AddField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(verbose_name='Date', default=datetime.datetime(2014, 11, 30, 4, 40, 20, 568115, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(verbose_name='Commentez'),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='branchmembers',
            options={'ordering': ['-is_admin']},
        ),
        migrations.AlterField(
            model_name='branch',
            name='location',
            field=models.CharField(null=True, verbose_name='Address', max_length=256, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(verbose_name="Branch's name", max_length=255, help_text='Nom de la localité'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='location',
            field=models.CharField(null=True, verbose_name='Adresse', max_length=256, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(verbose_name='Nom de la branche', max_length=255, help_text='Nom de la localité'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='location',
            field=models.CharField(null=True, verbose_name='Address', max_length=256, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(verbose_name="Branch's name", max_length=255, help_text='Nom de la localité'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='location',
            field=models.CharField(null=True, verbose_name='Adresse', max_length=256, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(verbose_name='Nom de la branche', max_length=255, help_text='Nom de la localité'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='DemandProposition',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('comment', models.TextField(verbose_name='Commentaire')),
                ('created', models.DateTimeField(verbose_name="date d'arrivé", auto_now=True)),
                ('accepted', models.BooleanField(verbose_name='Proposition acceptée', default=False)),
                ('demand', models.ForeignKey(related_name='propositions', to='branch.Demand')),
                ('user', models.ForeignKey(related_name='propositions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='demand',
            name='volunteers',
            field=models.ManyToManyField(null=True, verbose_name='Propositions', through='branch.DemandProposition', related_name='volunteers', blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='location',
            field=models.CharField(null=True, verbose_name='Address', max_length=256, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(verbose_name="Branch's name", max_length=255, help_text='Nom de la localité'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='location',
            field=models.CharField(null=True, verbose_name='Address', max_length=256, blank=True),
            preserve_default=True,
        ),
    ]

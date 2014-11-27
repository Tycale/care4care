# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re
from django.conf import settings
import multiselectfield.db.fields
import django.core.validators
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('first_name', models.CharField(verbose_name='Prénom', max_length=30)),
                ('last_name', models.CharField(verbose_name='Nom', max_length=30)),
                ('location', models.CharField(null=True, blank=True, verbose_name='Adresse', max_length=256)),
                ('latitude', models.CharField(null=True, blank=True, verbose_name='Latitude', max_length=20)),
                ('longitude', models.CharField(null=True, blank=True, verbose_name='Longitude', max_length=20)),
                ('phone_number', models.CharField(blank=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.")], verbose_name='Numéro de téléphone (fixe)', max_length=16)),
                ('mobile_number', models.CharField(blank=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.")], verbose_name='Numéro de téléphone mobile', max_length=16)),
                ('languages', multiselectfield.db.fields.MultiSelectField(blank=True, verbose_name='Langues parlées', choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')], max_length=8)),
                ('email', models.EmailField(blank=True, verbose_name='Adresse email', max_length=75)),
                ('relationship', models.CharField(blank=True, verbose_name='Votre relation par rapport à cette personne', max_length=255)),
                ('comments', models.CharField(blank=True, verbose_name='Commentaire supplémentaire', max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmergencyContact',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('first_name', models.CharField(verbose_name='Prénom', max_length=30)),
                ('last_name', models.CharField(verbose_name='Nom', max_length=30)),
                ('location', models.CharField(null=True, blank=True, verbose_name='Adresse', max_length=256)),
                ('latitude', models.CharField(null=True, blank=True, verbose_name='Latitude', max_length=20)),
                ('longitude', models.CharField(null=True, blank=True, verbose_name='Longitude', max_length=20)),
                ('phone_number', models.CharField(blank=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.")], verbose_name='Numéro de téléphone (fixe)', max_length=16)),
                ('mobile_number', models.CharField(blank=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.")], verbose_name='Numéro de téléphone mobile', max_length=16)),
                ('languages', multiselectfield.db.fields.MultiSelectField(blank=True, verbose_name='Langues parlées', choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')], max_length=8)),
                ('order', models.IntegerField(verbose_name='Ordre de priorité', default=0, choices=[(1, 'A contacter en premier'), (2, 'A contacter'), (3, 'A contacter en dernier')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VerifiedInformation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('recomendation_letter_1', models.FileField(null=True, upload_to='documents/', verbose_name='Lettre de recommendation n°1')),
                ('recomendation_letter_2', models.FileField(null=True, upload_to='documents/', verbose_name='Lettre de recommendation n°2')),
                ('criminal_record', models.FileField(null=True, upload_to='documents/', verbose_name='Casier judiciaire')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VerifiedUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('have_car', models.BooleanField(verbose_name="Disposez-vous d'une voiture ?", default=False, choices=[(True, 'Oui'), (False, 'Non')])),
                ('can_wheelchair', models.BooleanField(verbose_name='Pouvez-vous transporter une chaise roulante dans votre voiture ?', default=False, choices=[(True, 'Oui'), (False, 'Non')])),
                ('drive_license', multiselectfield.db.fields.MultiSelectField(blank=True, verbose_name='Type de permis de conduire', choices=[(1, 'Vélomoteur'), (2, 'Moto'), (3, 'Voiture'), (4, 'Camion'), (5, 'Bus'), (6, 'Tracteur')], max_length=11)),
                ('mail_preferences', models.IntegerField(verbose_name='Recevoir mes messages par', default=1, choices=[(1, 'Boite à message'), (2, 'Mail')])),
                ('receive_help_from_who', models.IntegerField(verbose_name='Recevoir des demandes et des offres de', default=5, choices=[(5, 'Tous'), (3, 'Membre vérifié'), (6, 'Favoris (inclus le réseau personnel)')])),
                ('offered_job', multiselectfield.db.fields.MultiSelectField(blank=True, verbose_name='Quelles sont les tâches que vous souhaitez effectuer ?', choices=[(1, 'Visite à la maison'), (2, 'Tenir compagnie'), (3, 'Transport par voiture'), (4, 'Shopping'), (5, 'Garder des maisons'), (6, 'Petits boulots manuels'), (7, 'Jardinage'), (8, 'Garder des animaux'), (9, 'Soins personnels'), (10, 'Administratif'), (11, 'Autre'), (12, 'Spécial ... :D')], max_length=26)),
                ('asked_job', multiselectfield.db.fields.MultiSelectField(blank=True, verbose_name='Quelles sont les tâches dont vous avez besoin ?', choices=[(1, 'Visite à la maison'), (2, 'Tenir compagnie'), (3, 'Transport par voiture'), (4, 'Shopping'), (5, 'Garder des maisons'), (6, 'Petits boulots manuels'), (7, 'Jardinage'), (8, 'Garder des animaux'), (9, 'Soins personnels'), (10, 'Administratif'), (11, 'Autre'), (12, 'Spécial ... :D')], max_length=26)),
                ('facebook', models.URLField(blank=True, verbose_name='Lien (URL) de votre profil Facebook')),
                ('hobbies', models.TextField(blank=True, verbose_name='Vos hobbies')),
                ('additional_info', models.TextField(blank=True, verbose_name='Informations supplémentaires')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('verifieduser_ptr', models.OneToOneField(to='main.VerifiedUser', serialize=False, auto_created=True, primary_key=True, parent_link=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('first_name', models.CharField(verbose_name='Prénom', max_length=30)),
                ('last_name', models.CharField(verbose_name='Nom', max_length=30)),
                ('location', models.CharField(null=True, blank=True, verbose_name='Adresse', max_length=256)),
                ('latitude', models.CharField(null=True, blank=True, verbose_name='Latitude', max_length=20)),
                ('longitude', models.CharField(null=True, blank=True, verbose_name='Longitude', max_length=20)),
                ('phone_number', models.CharField(blank=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.")], verbose_name='Numéro de téléphone (fixe)', max_length=16)),
                ('mobile_number', models.CharField(blank=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.")], verbose_name='Numéro de téléphone mobile', max_length=16)),
                ('languages', multiselectfield.db.fields.MultiSelectField(blank=True, verbose_name='Langues parlées', choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')], max_length=8)),
                ('email', models.EmailField(verbose_name='Adresse email', max_length=75)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), "Entrez un nom d'utilisateur valide.             30 caractères ou moins. Peut contenir des lettres, nombres et les caractères @/./+/-/_ ", 'invalid')], verbose_name='Username', max_length=30)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('status', models.IntegerField(default=1, choices=[(1, 'Actif'), (2, 'En vacance'), (3, 'Désactivé')])),
                ('user_type', models.IntegerField(help_text="Un member pourra aider ou être aidé alors qu'un                                        non-membre est un professionnel qui s'inscrira pour avoir accès aux données d'un                                        patient. Veuillez choisir celui qui vous correspond", verbose_name='Type de compte', default=1, choices=[(1, 'Membre'), (2, 'Non-membre')])),
                ('how_found', multiselectfield.db.fields.MultiSelectField(verbose_name='Comment avez-vous entendu parler de Care4Care ?', max_length=15, choices=[('amis', "Mes amis m'en ont parlés"), ('pubs', "J'ai vu de la pub"), ('other', 'Autre')])),
                ('birth_date', models.DateField(null=True, blank=True, verbose_name='Date de naissance')),
                ('credit', models.IntegerField(verbose_name='Crédit restant', default=0)),
                ('organization', models.CharField(blank=True, verbose_name='Organization', max_length=100)),
                ('work', models.CharField(null=True, blank=True, verbose_name='Fonction', max_length=100)),
                ('groups', models.ManyToManyField(to='auth.Group', related_name='user_set', related_query_name='user', blank=True, verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.')),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', related_name='user_set', related_query_name='user', blank=True, verbose_name='user permissions', help_text='Specific permissions for this user.')),
            ],
            options={
                'abstract': False,
            },
            bases=('main.verifieduser', models.Model),
        ),
        migrations.AddField(
            model_name='verifieduser',
            name='favorites',
            field=models.ManyToManyField(null=True, related_name='verified_favorites', blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='verifieduser',
            name='personal_network',
            field=models.ManyToManyField(null=True, related_name='verified_personal_network', blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Votre réseau personnel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='verifieduser',
            name='work_with',
            field=models.ManyToManyField(null=True, related_name='verified_work_with', blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='verifiedinformation',
            name='user',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emergencycontact',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='emergency_contacts'),
            preserve_default=True,
        ),
    ]

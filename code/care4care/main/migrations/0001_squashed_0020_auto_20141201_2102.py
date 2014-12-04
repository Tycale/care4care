# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
import django.core.validators
import datetime
import re
import easy_thumbnails.fields
import django.utils.timezone
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    #replaces = [('main', '0001_initial'), ('main', '0002_auto_20141127_1044'), ('main', '0003_auto_20141127_1356'), ('main', '0004_auto_20141128_1624'), ('main', '0004_auto_20141128_1621'), ('main', '0005_merge'), ('main', '0006_auto_20141129_0939'), ('main', '0007_auto_20141129_1140'), ('main', '0006_auto_20141129_1015'), ('main', '0008_merge'), ('main', '0008_auto_20141129_1410'), ('main', '0009_merge'), ('main', '0010_auto_20141129_1611'), ('main', '0011_auto_20141129_1730'), ('main', '0012_auto_20141129_1803'), ('main', '0013_auto_20141129_1831'), ('main', '0014_auto_20141129_2018'), ('main', '0015_auto_20141129_2113'), ('main', '0016_auto_20141130_1904'), ('main', '0017_auto_20141130_2043'), ('main', '0018_auto_20141201_0017'), ('main', '0019_auto_20141201_1201'), ('main', '0020_auto_20141201_2102')]

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('first_name', models.CharField(max_length=30, verbose_name='First name')),
                ('last_name', models.CharField(max_length=30, verbose_name='Name')),
                ('location', models.CharField(blank=True, max_length=256, verbose_name='Address', null=True)),
                ('latitude', models.CharField(blank=True, max_length=20, verbose_name='Latitude', null=True)),
                ('longitude', models.CharField(blank=True, max_length=20, verbose_name='Longitude', null=True)),
                ('phone_number', models.CharField(max_length=16, blank=True, validators=[django.core.validators.RegexValidator(message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Numéro de téléphone (fixe)')),
                ('mobile_number', models.CharField(max_length=16, blank=True, validators=[django.core.validators.RegexValidator(message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Numéro de téléphone (mobile)')),
                ('languages', multiselectfield.db.fields.MultiSelectField(verbose_name='Spoken languages', blank=True, max_length=8, choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')])),
                ('email', models.EmailField(blank=True, max_length=75, verbose_name='Adresse email')),
                ('relationship', models.CharField(blank=True, max_length=255, verbose_name='Votre relation par rapport à cette personne')),
                ('comments', models.CharField(blank=True, max_length=255, verbose_name='Commentaire supplémentaire')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmergencyContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('first_name', models.CharField(max_length=30, verbose_name='Prénom')),
                ('last_name', models.CharField(max_length=30, verbose_name='Nom')),
                ('location', models.CharField(blank=True, max_length=256, verbose_name='Adresse', null=True)),
                ('latitude', models.CharField(blank=True, max_length=20, verbose_name='Latitude', null=True)),
                ('longitude', models.CharField(blank=True, max_length=20, verbose_name='Longitude', null=True)),
                ('phone_number', models.CharField(max_length=16, blank=True, validators=[django.core.validators.RegexValidator(message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Numéro de téléphone (fixe)')),
                ('mobile_number', models.CharField(max_length=16, blank=True, validators=[django.core.validators.RegexValidator(message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Numéro de téléphone mobile')),
                ('languages', multiselectfield.db.fields.MultiSelectField(verbose_name='Langues parlées', blank=True, max_length=8, choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')])),
                ('order', models.IntegerField(default=0, verbose_name='Ordre de priorité', choices=[(1, 'A contacter en premier'), (2, 'A contacter'), (3, 'A contacter en dernier')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VerifiedInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('recomendation_letter_1', models.FileField(null=True, verbose_name='Lettre de recommendation n°1', upload_to='documents/')),
                ('recomendation_letter_2', models.FileField(null=True, verbose_name='Lettre de recommendation n°2', upload_to='documents/')),
                ('criminal_record', models.FileField(null=True, verbose_name='Casier judiciaire', upload_to='documents/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VerifiedUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('have_car', models.BooleanField(default=False, verbose_name="Disposez-vous d'une voiture ?", choices=[(True, 'Oui'), (False, 'Non')])),
                ('can_wheelchair', models.BooleanField(default=False, verbose_name='Pouvez-vous transporter une chaise roulante dans votre voiture ?', choices=[(True, 'Oui'), (False, 'Non')])),
                ('drive_license', multiselectfield.db.fields.MultiSelectField(verbose_name='Type de permis de conduire', blank=True, max_length=11, choices=[(1, 'Vélomoteur'), (2, 'Moto'), (3, 'Voiture'), (4, 'Camion'), (5, 'Bus'), (6, 'Tracteur')])),
                ('mail_preferences', models.IntegerField(default=1, verbose_name='Recevoir mes messages par', choices=[(1, 'Boite à message'), (2, 'Mail')])),
                ('receive_help_from_who', models.IntegerField(default=5, verbose_name='Recevoir des demandes et des offres de', choices=[(5, 'Tous'), (3, 'Membre vérifié'), (6, 'Favoris (inclus le réseau personnel)')])),
                ('offered_job', multiselectfield.db.fields.MultiSelectField(verbose_name='Quelles sont les tâches que vous souhaitez effectuer ?', blank=True, max_length=26, choices=[(1, 'Visite à la maison'), (2, 'Tenir compagnie'), (3, 'Transport par voiture'), (4, 'Shopping'), (5, 'Garder des maisons'), (6, 'Petits boulots manuels'), (7, 'Jardinage'), (8, 'Garder des animaux'), (9, 'Soins personnels'), (10, 'Administratif'), (11, 'Autre'), (12, 'Spécial ... :D')])),
                ('asked_job', multiselectfield.db.fields.MultiSelectField(verbose_name='Quelles sont les tâches dont vous avez besoin ?', blank=True, max_length=26, choices=[(1, 'Visite à la maison'), (2, 'Tenir compagnie'), (3, 'Transport par voiture'), (4, 'Shopping'), (5, 'Garder des maisons'), (6, 'Petits boulots manuels'), (7, 'Jardinage'), (8, 'Garder des animaux'), (9, 'Soins personnels'), (10, 'Administratif'), (11, 'Autre'), (12, 'Spécial ... :D')])),
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
                ('verifieduser_ptr', models.OneToOneField(parent_link=True, primary_key=True, serialize=False, auto_created=True, to='main.VerifiedUser')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('first_name', models.CharField(max_length=30, verbose_name='First name')),
                ('last_name', models.CharField(max_length=30, verbose_name='Name')),
                ('location', models.CharField(blank=True, max_length=256, verbose_name='Address', null=True)),
                ('latitude', models.CharField(blank=True, max_length=20, verbose_name='Latitude', null=True)),
                ('longitude', models.CharField(blank=True, max_length=20, verbose_name='Longitude', null=True)),
                ('phone_number', models.CharField(max_length=16, blank=True, validators=[django.core.validators.RegexValidator(message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Numéro de téléphone (fixe)')),
                ('mobile_number', models.CharField(max_length=16, blank=True, validators=[django.core.validators.RegexValidator(message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Numéro de téléphone (mobile)')),
                ('languages', multiselectfield.db.fields.MultiSelectField(verbose_name='Spoken languages', blank=True, max_length=8, choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')])),
                ('email', models.EmailField(max_length=75, verbose_name='Adresse email')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(unique=True, max_length=30, validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), "Entrez un nom d'utilisateur valide.             30 caractères ou moins. Peut contenir des lettres, nombres et les caractères @/./+/-/_ ", 'invalid')], verbose_name='Username')),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('status', models.IntegerField(default=1, choices=[(1, 'Actif'), (2, 'En vacances'), (3, 'Désactivé')])),
                ('user_type', models.IntegerField(default=1, help_text="Un member pourra aider ou être aidé alors qu'un                                         non-membre est un professionnel qui s'inscrira pour avoir accès aux données d'un                                         patient. Veuillez choisir celui qui vous correspond", choices=[(1, 'Membre'), (2, 'Non-membre')], verbose_name='Type de compte')),
                ('how_found', multiselectfield.db.fields.MultiSelectField(verbose_name='Comment avez-vous entendu parler de Care4Care ?', max_length=41, choices=[('internet', 'Internet'), ('show', 'Présentation, brochures, flyers, ...'), ('branch', 'Par une branche locale'), ('member', 'Un autre membre'), ('friends', "Des amis ou de la famille m'en ont parlés"), ('other', 'Autre')])),
                ('birth_date', models.DateField(blank=True, verbose_name='Date de naissance', null=True)),
                ('credit', models.IntegerField(verbose_name='Crédit restant', default=0)),
                ('organization', models.CharField(blank=True, max_length=100, verbose_name='Organization')),
                ('work', models.CharField(blank=True, max_length=100, verbose_name='Fonction', null=True)),
                ('groups', models.ManyToManyField(related_query_name='user', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions', related_name='user_set')),
                ('photo', easy_thumbnails.fields.ThumbnailerImageField(default='photos/default_avatar.png', upload_to='photos/')),
            ],
            options={
                'abstract': False,
            },
            bases=('main.verifieduser', models.Model),
        ),
        migrations.AddField(
            model_name='verifieduser',
            name='favorites',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, null=True, related_name='verified_favorites'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='verifieduser',
            name='personal_network',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, verbose_name='Votre réseau personnel', null=True, related_name='verified_personal_network'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='verifieduser',
            name='work_with',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, null=True, related_name='verified_work_with'),
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
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Langues parlées', blank=True, max_length=8, choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')]),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='emergencycontact',
            options={'ordering': ['order']},
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='mobile_number',
            field=models.CharField(max_length=16, blank=True, validators=[django.core.validators.RegexValidator(message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Numéro de téléphone (mobile)'),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='emergencycontact',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='verifieduser',
            name='ignore_list',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, verbose_name='Personne ignorée', null=True, related_name='verified_ignore_list'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='mobile_number',
            field=models.CharField(max_length=16, blank=True, validators=[django.core.validators.RegexValidator(message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Numéro de téléphone (mobile)'),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='verifiedinformation',
            options={'ordering': ['date']},
        ),
        migrations.AddField(
            model_name='verifiedinformation',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 29, 9, 39, 9, 486026, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='additional_info',
            field=models.TextField(blank=True, max_length=300, verbose_name='Informations supplémentaires'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='hobbies',
            field=models.TextField(blank=True, max_length=200, verbose_name='Vos hobbies'),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='verifiedinformation',
            options={'ordering': ['date']},
        ),
        migrations.AddField(
            model_name='verifiedinformation',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 29, 10, 15, 29, 899409, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Langues parlées', blank=True, max_length=8, choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Langues parlées', blank=True, max_length=8, choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Langues parlées', blank=True, max_length=8, choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Langues parlées', blank=True, max_length=8, choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Langues parlées', blank=True, max_length=8, choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Langues parlées', blank=True, max_length=8, choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Langues parlées', blank=True, max_length=8, choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='First name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Spoken languages', blank=True, max_length=8, choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='location',
            field=models.CharField(blank=True, max_length=256, verbose_name='Address', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='Prénom'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Langues parlées', blank=True, max_length=8, choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='Nom'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='location',
            field=models.CharField(blank=True, max_length=256, verbose_name='Adresse', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='First name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Spoken languages', blank=True, max_length=8, choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='location',
            field=models.CharField(blank=True, max_length=256, verbose_name='Address', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='Prénom'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Langues parlées', blank=True, max_length=8, choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='Nom'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='location',
            field=models.CharField(blank=True, max_length=256, verbose_name='Adresse', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='First name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Spoken languages', blank=True, max_length=8, choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='location',
            field=models.CharField(blank=True, max_length=256, verbose_name='Address', null=True),
            preserve_default=True,
        ),
    ]

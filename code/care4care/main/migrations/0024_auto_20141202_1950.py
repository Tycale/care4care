# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
import re
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_auto_20141202_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='comments',
            field=models.CharField(verbose_name='Commentaire supplémentaire', max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(verbose_name='Adresse email', max_length=75, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='first_name',
            field=models.CharField(verbose_name='Prénom', max_length=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')], verbose_name='Langues parlées', max_length=8, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='last_name',
            field=models.CharField(verbose_name='Nom', max_length=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='location',
            field=models.CharField(verbose_name='Adresse', max_length=256, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='mobile_number',
            field=models.CharField(verbose_name='Numéro de téléphone (mobile)', max_length=16, validators=[django.core.validators.RegexValidator(message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.", regex='^\\+?1?\\d{9,15}$')], blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone_number',
            field=models.CharField(verbose_name='Numéro de téléphone (fixe)', max_length=16, validators=[django.core.validators.RegexValidator(message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.", regex='^\\+?1?\\d{9,15}$')], blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='relationship',
            field=models.CharField(verbose_name='Votre relation par rapport à cette personne', max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='first_name',
            field=models.CharField(verbose_name='Prénom', max_length=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')], verbose_name='Langues parlées', max_length=8, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='last_name',
            field=models.CharField(verbose_name='Nom', max_length=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='location',
            field=models.CharField(verbose_name='Adresse', max_length=256, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='mobile_number',
            field=models.CharField(verbose_name='Numéro de téléphone (mobile)', max_length=16, validators=[django.core.validators.RegexValidator(message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.", regex='^\\+?1?\\d{9,15}$')], blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='order',
            field=models.IntegerField(choices=[(1, 'A contacter en premier'), (2, 'A contacter'), (3, 'A contacter en dernier')], verbose_name='Ordre de priorité', default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='phone_number',
            field=models.CharField(verbose_name='Numéro de téléphone (fixe)', max_length=16, validators=[django.core.validators.RegexValidator(message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.", regex='^\\+?1?\\d{9,15}$')], blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(verbose_name='Date de naissance', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='credit',
            field=models.IntegerField(verbose_name='Crédit restant', default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(verbose_name='Adresse email', max_length=75),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(verbose_name='Prénom', max_length=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='how_found',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('internet', 'Internet'), ('show', 'Présentation, brochures, flyers, ...'), ('branch', 'Par une branche locale'), ('member', 'Un autre membre'), ('friends', "Des amis ou de la famille m'en ont parlés"), ('other', 'Autre')], verbose_name='Comment avez-vous entendu parler de Care4Care ?', max_length=41),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')], verbose_name='Langues parlées', max_length=8, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(verbose_name='Nom', max_length=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.CharField(verbose_name='Adresse', max_length=256, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile_number',
            field=models.CharField(verbose_name='Numéro de téléphone (mobile)', max_length=16, validators=[django.core.validators.RegexValidator(message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.", regex='^\\+?1?\\d{9,15}$')], blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(verbose_name='Numéro de téléphone (fixe)', max_length=16, validators=[django.core.validators.RegexValidator(message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.", regex='^\\+?1?\\d{9,15}$')], blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.IntegerField(choices=[(1, 'Actif'), (2, 'En vacances'), (3, 'Désactivé')], default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(choices=[(1, 'Membre'), (2, 'Non-membre')], verbose_name='Type de compte', help_text="Un member pourra aider ou être aidé alors qu'un                                         non-membre est un professionnel qui s'inscrira pour avoir accès aux données d'un                                         patient. Veuillez choisir celui qui vous correspond", default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(unique=True, verbose_name="Nom d'utilisateur", max_length=30, validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), "Entrez un nom d'utilisateur valide.             30 caractères ou moins. Peut contenir des lettres, nombres et les caractères @/./+/-/_ ", 'invalid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifiedinformation',
            name='criminal_record',
            field=models.FileField(verbose_name='Casier judiciaire', null=True, upload_to='documents/'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifiedinformation',
            name='recomendation_letter_1',
            field=models.FileField(verbose_name='Lettre de recommendation n°1', null=True, upload_to='documents/'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifiedinformation',
            name='recomendation_letter_2',
            field=models.FileField(verbose_name='Lettre de recommendation n°2', null=True, upload_to='documents/'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='additional_info',
            field=models.TextField(verbose_name='Informations supplémentaires', max_length=300, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='asked_job',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('1', 'Visite à la maison'), ('2', 'Tenir compagnie'), ('3', 'Transport par voiture'), ('4', 'Shopping'), ('5', 'Garder des maisons'), ('6', 'Petits boulots manuels'), ('7', 'Jardinage'), ('8', 'Garder des animaux'), ('9', 'Soins personnels'), ('a', 'Administratif'), ('b', 'Autre')], verbose_name='Quelles sont les tâches dont vous avez besoin ?', max_length=21, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='can_wheelchair',
            field=models.BooleanField(choices=[(True, 'Oui'), (False, 'Non')], verbose_name='Pouvez-vous transporter une chaise roulante dans votre voiture ?', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='drive_license',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Vélomoteur'), (2, 'Moto'), (3, 'Voiture'), (4, 'Camion'), (5, 'Bus'), (6, 'Tracteur')], verbose_name='Type de permis de conduire', max_length=11, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='have_car',
            field=models.BooleanField(choices=[(True, 'Oui'), (False, 'Non')], verbose_name="Disposez-vous d'une voiture ?", default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='hobbies',
            field=models.TextField(verbose_name='Vos hobbies', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='mail_preferences',
            field=models.IntegerField(choices=[(1, 'Boite à message'), (2, 'Mail')], verbose_name='Recevoir mes messages par', default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='offered_job',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('1', 'Visite à la maison'), ('2', 'Tenir compagnie'), ('3', 'Transport par voiture'), ('4', 'Shopping'), ('5', 'Garder des maisons'), ('6', 'Petits boulots manuels'), ('7', 'Jardinage'), ('8', 'Garder des animaux'), ('9', 'Soins personnels'), ('a', 'Administratif'), ('b', 'Autre')], verbose_name='Quelles sont les tâches que vous souhaitez effectuer ?', max_length=21, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='receive_help_from_who',
            field=models.IntegerField(choices=[(5, 'Tous'), (3, 'Membre vérifié'), (6, 'Favoris (inclus le réseau personnel)')], verbose_name='Recevoir des demandes et des offres de', default=5),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re
import django.core.validators
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_auto_20141204_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='comments',
            field=models.CharField(blank=True, max_length=255, verbose_name='Commentaire supplémentaire'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(blank=True, max_length=75, verbose_name='Adresse email'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='Prénom'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=8, choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')], verbose_name='Langues parlées'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='Nom'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='location',
            field=models.CharField(blank=True, null=True, max_length=256, verbose_name='Adresse'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='mobile_number',
            field=models.CharField(blank=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.")], max_length=16, verbose_name='Numéro de téléphone (mobile)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone_number',
            field=models.CharField(blank=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.")], max_length=16, verbose_name='Numéro de téléphone (fixe)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='relationship',
            field=models.CharField(blank=True, max_length=255, verbose_name='Votre relation par rapport à cette personne'),
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
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=8, choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')], verbose_name='Langues parlées'),
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
            field=models.CharField(blank=True, null=True, max_length=256, verbose_name='Adresse'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='mobile_number',
            field=models.CharField(blank=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.")], max_length=16, verbose_name='Numéro de téléphone (mobile)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='order',
            field=models.IntegerField(default=0, choices=[(1, 'A contacter en premier'), (2, 'A contacter'), (3, 'A contacter en dernier')], verbose_name='Ordre de priorité'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='phone_number',
            field=models.CharField(blank=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.")], max_length=16, verbose_name='Numéro de téléphone (fixe)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Date de naissance'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='credit',
            field=models.IntegerField(default=0, verbose_name='Crédit restant'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=75, verbose_name='Adresse email'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='Prénom'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='how_found',
            field=multiselectfield.db.fields.MultiSelectField(max_length=41, choices=[('internet', 'Internet'), ('show', 'Présentation, brochures, flyers, ...'), ('branch', 'Par une branche locale'), ('member', 'Un autre membre'), ('friends', "Des amis ou de la famille m'en ont parlés"), ('other', 'Autre')], verbose_name='Comment avez-vous entendu parler de Care4Care ?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=8, choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')], verbose_name='Langues parlées'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='Nom'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.CharField(blank=True, null=True, max_length=256, verbose_name='Adresse'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile_number',
            field=models.CharField(blank=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.")], max_length=16, verbose_name='Numéro de téléphone (mobile)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.")], max_length=16, verbose_name='Numéro de téléphone (fixe)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.IntegerField(default=1, choices=[(1, 'Actif'), (2, 'En vacances'), (3, 'Désactivé')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(help_text="Un member pourra aider ou être aidé alors qu'un                                         non-membre est un professionnel qui s'inscrira pour avoir accès aux données d'un                                         patient. Veuillez choisir celui qui vous correspond", default=1, choices=[(1, 'Membre'), (2, 'Non-membre'), (3, 'Membre vérifié')], verbose_name='Type de compte'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), "Entrez un nom d'utilisateur valide.             30 caractères ou moins. Peut contenir des lettres, nombres et les caractères @/./+/-/_ ", 'invalid')], max_length=30, verbose_name="Nom d'utilisateur", unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifiedinformation',
            name='criminal_record',
            field=models.FileField(null=True, verbose_name='Casier judiciaire', upload_to='documents/'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifiedinformation',
            name='recomendation_letter_1',
            field=models.FileField(null=True, verbose_name='Lettre de recommendation n°1', upload_to='documents/'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifiedinformation',
            name='recomendation_letter_2',
            field=models.FileField(null=True, verbose_name='Lettre de recommendation n°2', upload_to='documents/'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='additional_info',
            field=models.TextField(blank=True, max_length=300, verbose_name='Informations supplémentaires'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='can_wheelchair',
            field=models.BooleanField(default=False, choices=[(True, 'Oui'), (False, 'Non')], verbose_name='Pouvez-vous transporter une chaise roulante dans votre voiture ?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='drive_license',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=11, choices=[(1, 'Vélomoteur'), (2, 'Moto'), (3, 'Voiture'), (4, 'Camion'), (5, 'Bus'), (6, 'Tracteur')], verbose_name='Type de permis de conduire'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='have_car',
            field=models.BooleanField(default=False, choices=[(True, 'Oui'), (False, 'Non')], verbose_name="Disposez-vous d'une voiture ?"),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='hobbies',
            field=models.TextField(blank=True, max_length=200, verbose_name='Vos hobbies'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='mail_preferences',
            field=models.IntegerField(default=1, choices=[(1, 'Boite à message'), (2, 'Mail')], verbose_name='Recevoir mes messages par'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='offered_job',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=21, choices=[('1', 'Visite à la maison'), ('2', 'Tenir compagnie'), ('3', 'Transport par voiture'), ('4', 'Shopping'), ('5', 'Garder des maisons'), ('6', 'Petits boulots manuels'), ('7', 'Jardinage'), ('8', 'Garder des animaux'), ('9', 'Soins personnels'), ('a', 'Administratif'), ('b', 'Autre')], verbose_name='Quelles sont les tâches que vous souhaitez effectuer ?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='receive_help_from_who',
            field=models.IntegerField(default=5, choices=[(5, 'Tous'), (3, 'Membre vérifié'), (6, 'Mes membres favoris')], verbose_name='Recevoir des demandes et des offres de'),
            preserve_default=True,
        ),
    ]

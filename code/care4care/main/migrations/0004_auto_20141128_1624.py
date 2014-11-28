# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20141127_1356'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emergencycontact',
            options={'ordering': ['order']},
        ),
        migrations.AlterField(
            model_name='contact',
            name='mobile_number',
            field=models.CharField(validators=[django.core.validators.RegexValidator(message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.", regex='^\\+?1?\\d{9,15}$')], max_length=16, blank=True, verbose_name='Numéro de téléphone (mobile)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='mobile_number',
            field=models.CharField(validators=[django.core.validators.RegexValidator(message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.", regex='^\\+?1?\\d{9,15}$')], max_length=16, blank=True, verbose_name='Numéro de téléphone (mobile)'),
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
            name='mobile_number',
            field=models.CharField(validators=[django.core.validators.RegexValidator(message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.", regex='^\\+?1?\\d{9,15}$')], max_length=16, blank=True, verbose_name='Numéro de téléphone (mobile)'),
            preserve_default=True,
        ),
    ]

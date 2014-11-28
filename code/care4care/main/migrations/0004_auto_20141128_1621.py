# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
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
        migrations.AddField(
            model_name='verifieduser',
            name='ignore_list',
            field=models.ManyToManyField(related_name='verified_ignore_list', null=True, verbose_name='Personne ignorée', blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='mobile_number',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.")], verbose_name='Numéro de téléphone (mobile)', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='mobile_number',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.")], verbose_name='Numéro de téléphone (mobile)', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile_number',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Votre numéro de téléphone doit être au format '+999999999'. Jusqu'à 15 chiffres.")], verbose_name='Numéro de téléphone (mobile)', blank=True),
            preserve_default=True,
        ),
    ]

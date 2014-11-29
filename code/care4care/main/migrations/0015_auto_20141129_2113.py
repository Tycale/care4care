# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
import django.core.validators
import re


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20141129_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Langues parlées', max_length=8, blank=True, choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Langues parlées', max_length=8, blank=True, choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Langues parlées', max_length=8, blank=True, choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(verbose_name='Type de compte', default=1, choices=[(1, 'Membre'), (2, 'Non-membre')], help_text="Un member pourra aider ou être aidé alors qu'un                                         non-membre est un professionnel qui s'inscrira pour avoir accès aux données d'un                                         patient. Veuillez choisir celui qui vous correspond"),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(verbose_name='Username', validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), "Entrez un nom d'utilisateur valide.             30 caractères ou moins. Peut contenir des lettres, nombres et les caractères @/./+/-/_ ", 'invalid')], unique=True, max_length=30),
            preserve_default=True,
        ),
    ]

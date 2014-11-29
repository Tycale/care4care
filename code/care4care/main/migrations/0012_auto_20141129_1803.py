# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re
import multiselectfield.db.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20141129_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Langues parlées', blank=True, choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')], max_length=8),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Langues parlées', blank=True, choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')], max_length=8),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Langues parlées', blank=True, choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')], max_length=8),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), "Entrez un nom d'utilisateur valide.             30 caractères ou moins. Peut contenir des lettres, nombres et les caractères @/./+/-/_ ", 'invalid')], verbose_name="Nom d'utilisateur", unique=True, max_length=30),
            preserve_default=True,
        ),
    ]

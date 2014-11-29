# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re
import django.core.validators
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20141129_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Langues parlées', max_length=8, blank=True, choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Langues parlées', max_length=8, blank=True, choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Langues parlées', max_length=8, blank=True, choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), "Entrez un nom d'utilisateur valide.             30 caractères ou moins. Peut contenir des lettres, nombres et les caractères @/./+/-/_ ", 'invalid')], verbose_name="Nom d'utilisateur", max_length=30, unique=True),
            preserve_default=True,
        ),
    ]

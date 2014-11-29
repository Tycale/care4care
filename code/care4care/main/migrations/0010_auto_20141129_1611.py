# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
import re
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')], blank=True, verbose_name='Langues parlées', max_length=8),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')], blank=True, verbose_name='Langues parlées', max_length=8),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')], blank=True, verbose_name='Langues parlées', max_length=8),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, verbose_name="Nom d'utilisateur", validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), "Entrez un nom d'utilisateur valide.             30 caractères ou moins. Peut contenir des lettres, nombres et les caractères @/./+/-/_ ", 'invalid')], unique=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import re
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20141129_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')], max_length=8, blank=True, verbose_name='Langues parlées'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')], max_length=8, blank=True, verbose_name='Langues parlées'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')], max_length=8, blank=True, verbose_name='Langues parlées'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), "Entrez un nom d'utilisateur valide.             30 caractères ou moins. Peut contenir des lettres, nombres et les caractères @/./+/-/_ ", 'invalid')], unique=True, max_length=30, verbose_name='Username'),
            preserve_default=True,
        ),
    ]

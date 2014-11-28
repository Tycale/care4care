# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import multiselectfield.db.fields
import easy_thumbnails.fields
import re


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='photo',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='photos', blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, verbose_name='Langues parlées', max_length=8, choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, verbose_name='Langues parlées', max_length=8, choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, verbose_name='Langues parlées', max_length=8, choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(verbose_name="Nom d'utilisateur", max_length=30, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), "Entrez un nom d'utilisateur valide.             30 caractères ou moins. Peut contenir des lettres, nombres et les caractères @/./+/-/_ ", 'invalid')]),
            preserve_default=True,
        ),
    ]

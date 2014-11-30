# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
import re
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20141130_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='first_name',
            field=models.CharField(verbose_name='Prénom', max_length=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, verbose_name='Langues parlées', choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')], max_length=8),
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
            field=models.CharField(verbose_name='Adresse', blank=True, null=True, max_length=256),
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
            field=multiselectfield.db.fields.MultiSelectField(blank=True, verbose_name='Langues parlées', choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')], max_length=8),
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
            field=models.CharField(verbose_name='Adresse', blank=True, null=True, max_length=256),
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
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, verbose_name='Langues parlées', choices=[('fr', 'Français'), ('en', 'Anglais'), ('nl', 'Néerlandais')], max_length=8),
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
            field=models.CharField(verbose_name='Adresse', blank=True, null=True, max_length=256),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(verbose_name="Nom d'utilisateur", validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), "Entrez un nom d'utilisateur valide.             30 caractères ou moins. Peut contenir des lettres, nombres et les caractères @/./+/-/_ ", 'invalid')], unique=True, max_length=30),
            preserve_default=True,
        ),
    ]

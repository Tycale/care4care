# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import re
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20141130_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='First name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(max_length=8, blank=True, verbose_name='Spoken languages', choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='location',
            field=models.CharField(max_length=256, null=True, blank=True, verbose_name='Address'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='First name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(max_length=8, blank=True, verbose_name='Spoken languages', choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='location',
            field=models.CharField(max_length=256, null=True, blank=True, verbose_name='Address'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='First name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(max_length=8, blank=True, verbose_name='Spoken languages', choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.CharField(max_length=256, null=True, blank=True, verbose_name='Address'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, unique=True, verbose_name='Username', validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), "Entrez un nom d'utilisateur valide.             30 caractères ou moins. Peut contenir des lettres, nombres et les caractères @/./+/-/_ ", 'invalid')]),
            preserve_default=True,
        ),
    ]

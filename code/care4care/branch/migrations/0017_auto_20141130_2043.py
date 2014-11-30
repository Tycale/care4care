# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0016_auto_20141130_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='location',
            field=models.CharField(verbose_name='Adresse', blank=True, null=True, max_length=256),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(verbose_name='Nom de la branche', help_text='Nom de la localité', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='location',
            field=models.CharField(verbose_name='Adresse', blank=True, null=True, max_length=256),
            preserve_default=True,
        ),
    ]

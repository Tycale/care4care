# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0018_auto_20141201_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='location',
            field=models.CharField(blank=True, null=True, verbose_name='Adresse', max_length=256),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=255, help_text='Nom de la localité', verbose_name='Nom de la branche'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='location',
            field=models.CharField(blank=True, null=True, verbose_name='Adresse', max_length=256),
            preserve_default=True,
        ),
    ]

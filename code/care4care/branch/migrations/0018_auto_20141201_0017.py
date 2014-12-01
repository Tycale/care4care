# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0017_auto_20141130_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='location',
            field=models.CharField(max_length=256, null=True, blank=True, verbose_name='Address'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=255, verbose_name="Branch's name", help_text='Nom de la localité'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='location',
            field=models.CharField(max_length=256, null=True, blank=True, verbose_name='Address'),
            preserve_default=True,
        ),
    ]

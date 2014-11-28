# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0002_auto_20141127_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='date',
            field=models.DateTimeField(verbose_name='Date (DD/MM/YYYY)', help_text="La date doit être indiquée sous le format DD/MM/YYYY où DD est le jour, MM est le mois et YYYY est l'année."),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='job',
            name='estimated_time',
            field=models.IntegerField(verbose_name='Temps estimé (en minutes)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='job',
            name='real_time',
            field=models.IntegerField(verbose_name='Temps réel (en minutes)'),
            preserve_default=True,
        ),
    ]

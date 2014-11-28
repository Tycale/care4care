# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0003_auto_20141127_0309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.TextField(verbose_name='Description', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='job',
            name='km',
            field=models.IntegerField(verbose_name='km', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='job',
            name='real_time',
            field=models.IntegerField(verbose_name='Temps réel (en minutes)', null=True, blank=True),
            preserve_default=True,
        ),
    ]

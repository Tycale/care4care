# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0020_auto_20141201_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='demandproposition',
            name='km',
            field=models.IntegerField(null=True, verbose_name='Distance depuis domicile', blank=True),
            preserve_default=True,
        ),
    ]

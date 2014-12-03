# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0022_auto_20141201_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='demand',
            name='closed',
            field=models.BooleanField(default=False, verbose_name='Vontaire assigné'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demandproposition',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='uservol'),
            preserve_default=True,
        ),
    ]

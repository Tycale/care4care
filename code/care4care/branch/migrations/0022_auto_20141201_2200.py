# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0021_demandproposition_km'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demandproposition',
            name='comment',
            field=models.TextField(verbose_name='Commentaire (facultatif)', blank=True, null=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0030_auto_20141203_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='demand',
            name='success_fill',
            field=models.BooleanField(verbose_name='Demande de confirmation envoyée', default=False),
            preserve_default=True,
        ),
    ]

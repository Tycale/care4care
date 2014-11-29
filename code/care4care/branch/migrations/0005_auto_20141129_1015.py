# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0004_auto_20141127_0310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='date',
            field=models.DateTimeField(verbose_name='Date'),
            preserve_default=True,
        ),
    ]

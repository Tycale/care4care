# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0015_auto_20141130_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='date',
            field=models.DateTimeField(verbose_name='Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='date',
            field=models.DateTimeField(verbose_name='Date'),
            preserve_default=True,
        ),
    ]

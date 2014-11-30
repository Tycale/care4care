# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0010_auto_20141129_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='estimated_time',
            field=models.IntegerField(null=True, verbose_name='Temps estimé (en minutes)', blank=True),
            preserve_default=True,
        ),
    ]

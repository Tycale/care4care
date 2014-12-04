# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0034_auto_20141204_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='success_fill',
            field=models.BooleanField(default=False, verbose_name='Confirmation request sent'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0034_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='successdemand',
            name='comment',
            field=models.TextField(null=True, blank=True, verbose_name='Comments'),
            preserve_default=True,
        ),
    ]

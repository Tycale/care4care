# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='corps',
            field=models.TextField(verbose_name='Body'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='date_debut',
            field=models.DateTimeField(verbose_name='Publication date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='date_fin',
            field=models.DateTimeField(null=True, blank=True, verbose_name='Expiration date (leave empty if no expiration desired)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='titre',
            field=models.CharField(max_length=250, verbose_name='Title'),
            preserve_default=True,
        ),
    ]

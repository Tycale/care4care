# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0014_auto_20141130_0440'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branchmembers',
            options={'ordering': ['-is_admin']},
        ),
        migrations.AlterField(
            model_name='branch',
            name='location',
            field=models.CharField(max_length=256, blank=True, verbose_name='Address', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(help_text='Nom de la localité', verbose_name="Branch's name", max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='date',
            field=models.DateField(verbose_name='Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='location',
            field=models.CharField(max_length=256, blank=True, verbose_name='Address', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='date',
            field=models.DateField(verbose_name='Date'),
            preserve_default=True,
        ),
    ]

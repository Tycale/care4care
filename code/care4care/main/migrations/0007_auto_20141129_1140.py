# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20141129_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifieduser',
            name='additional_info',
            field=models.TextField(blank=True, max_length=300, verbose_name='Informations supplémentaires'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='hobbies',
            field=models.TextField(blank=True, max_length=200, verbose_name='Vos hobbies'),
            preserve_default=True,
        ),
    ]

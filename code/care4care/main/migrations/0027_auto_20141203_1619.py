# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20141203_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifieduser',
            name='asked_job',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='What jobs you need?', max_length=21, choices=[('1', 'Visit home'), ('2', 'Companionship'), ('3', 'Transport by car'), ('4', 'Shopping'), ('5', 'House sitting'), ('6', 'Manual jobs'), ('7', 'Gardening'), ('8', 'Pet sitting'), ('9', 'Personal care'), ('a', 'Administrative'), ('b', 'Other ...')], blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='offered_job',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='What jobs you want to do?', max_length=21, choices=[('1', 'Visit home'), ('2', 'Companionship'), ('3', 'Transport by car'), ('4', 'Shopping'), ('5', 'House sitting'), ('6', 'Manual jobs'), ('7', 'Gardening'), ('8', 'Pet sitting'), ('9', 'Personal care'), ('a', 'Administrative'), ('b', 'Other ...')], blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='receive_help_from_who',
            field=models.IntegerField(verbose_name='Receive offers and demands', default=5, choices=[(5, 'All'), (3, 'Verified member'), (6, 'My favorite members')]),
            preserve_default=True,
        ),
    ]

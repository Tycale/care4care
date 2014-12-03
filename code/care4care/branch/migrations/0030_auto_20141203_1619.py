# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0029_auto_20141203_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Type of help', max_length=21, choices=[('1', 'Visit home'), ('2', 'Companionship'), ('3', 'Transport by car'), ('4', 'Shopping'), ('5', 'House sitting'), ('6', 'Manual jobs'), ('7', 'Gardening'), ('8', 'Pet sitting'), ('9', 'Personal care'), ('a', 'Administrative'), ('b', 'Other ...')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='receive_help_from_who',
            field=models.IntegerField(verbose_name='Who can see and respond to demand/offer', default=5, choices=[(5, 'All'), (3, 'Verified member'), (6, 'My favorite members')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='success',
            field=models.NullBooleanField(verbose_name='Succeded', default=None),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demandproposition',
            name='created',
            field=models.DateTimeField(verbose_name='Creation date', auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name='Type of help', max_length=21, choices=[('1', 'Visit home'), ('2', 'Companionship'), ('3', 'Transport by car'), ('4', 'Shopping'), ('5', 'House sitting'), ('6', 'Manual jobs'), ('7', 'Gardening'), ('8', 'Pet sitting'), ('9', 'Personal care'), ('a', 'Administrative'), ('b', 'Other ...')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='receive_help_from_who',
            field=models.IntegerField(verbose_name='Who can see and respond to demand/offer', default=5, choices=[(5, 'All'), (3, 'Verified member'), (6, 'My favorite members')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='successdemand',
            name='created',
            field=models.DateTimeField(verbose_name='Creation date', auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='successdemand',
            name='time',
            field=models.IntegerField(verbose_name='Time spent (in minutes)', blank=True, null=True),
            preserve_default=True,
        ),
    ]

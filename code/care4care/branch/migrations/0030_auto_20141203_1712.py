# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0029_auto_20141203_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('1', 'Visit home'), ('2', 'Companionship'), ('3', 'Transport by car'), ('4', 'Shopping'), ('5', 'House sitting'), ('6', 'Manual jobs'), ('7', 'Gardening'), ('8', 'Pet sitting'), ('9', 'Personal care'), ('a', 'Administrative'), ('b', 'Other ...')], max_length=21, verbose_name='Type of help'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='receive_help_from_who',
            field=models.IntegerField(default=5, choices=[(5, 'All'), (3, 'Verified member'), (6, 'My favorite members')], verbose_name='Who can see and respond to demand/offer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='success',
            field=models.NullBooleanField(default=None, verbose_name='Succeded'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demandproposition',
            name='created',
            field=models.DateTimeField(auto_now=True, verbose_name='Creation date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('1', 'Visit home'), ('2', 'Companionship'), ('3', 'Transport by car'), ('4', 'Shopping'), ('5', 'House sitting'), ('6', 'Manual jobs'), ('7', 'Gardening'), ('8', 'Pet sitting'), ('9', 'Personal care'), ('a', 'Administrative'), ('b', 'Other ...')], max_length=21, verbose_name='Type of help'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='receive_help_from_who',
            field=models.IntegerField(default=5, choices=[(5, 'All'), (3, 'Verified member'), (6, 'My favorite members')], verbose_name='Who can see and respond to demand/offer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='successdemand',
            name='ask_to',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='success_pending', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='successdemand',
            name='asked_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='approval_pending', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='successdemand',
            name='branch',
            field=models.ForeignKey(to='branch.Branch', null=True, related_name='success_branch_pending', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='successdemand',
            name='comment',
            field=models.TextField(null=True, blank=True, verbose_name='Comments'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='successdemand',
            name='created',
            field=models.DateTimeField(auto_now=True, verbose_name='Creation date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='successdemand',
            name='demand',
            field=models.ForeignKey(to='branch.Demand', null=True, related_name='success_demand', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='successdemand',
            name='time',
            field=models.IntegerField(null=True, blank=True, verbose_name='Time spent (in minutes)'),
            preserve_default=True,
        ),
    ]

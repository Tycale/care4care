# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0031_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='creator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Branch administrators'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='location',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Address'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='members',
            field=models.ManyToManyField(blank=True, null=True, through='branch.BranchMembers', verbose_name="Branch's members", related_name='members', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=255, verbose_name="Branch's name"),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branchmembers',
            name='joined',
            field=models.DateTimeField(verbose_name='Listing date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(verbose_name='Comment'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='branch',
            field=models.ForeignKey(verbose_name='Branch', to='branch.Branch', related_name='demand_branch'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(max_length=21, choices=[('1', 'Visit home'), ('2', 'Companionship'), ('3', 'Transport by car'), ('4', 'Shopping'), ('5', 'House sitting'), ('6', 'Manual jobs'), ('7', 'Gardening'), ('8', 'Pet sitting'), ('9', 'Personal care'), ('a', 'Administrative'), ('b', 'Other ...')], verbose_name='Type of help'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='closed',
            field=models.BooleanField(default=False, verbose_name='Assigned volunteer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='donor',
            field=models.ForeignKey(blank=True, related_name='demand_donor', verbose_name='Sender', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='estimated_time',
            field=models.IntegerField(blank=True, null=True, verbose_name='Estimetad time (in minutes)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='km',
            field=models.IntegerField(blank=True, null=True, verbose_name='Trip distance'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='location',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Address'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='real_time',
            field=models.IntegerField(blank=True, null=True, verbose_name='Real time (int minutes)'),
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
            name='receiver',
            field=models.ForeignKey(blank=True, related_name='demand_receiver', verbose_name='Receiver', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='time',
            field=multiselectfield.db.fields.MultiSelectField(max_length=17, choices=[(1, 'Early morning (8h-10h)'), (2, 'Late morning (10h-12h)'), (3, 'Noon (12h-13h)'), (4, 'Early afternoon (13h-16h)'), (5, 'Late afternoon (16h-19h)'), (6, 'Supper (19h-20h)'), (7, 'Early evening (20h-22h) '), (8, 'Late evening (22h-00h)'), (9, 'Night (00h-8h)')], verbose_name='Busy time', help_text='Select the hours that suit you'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='title',
            field=models.CharField(max_length=120, null=True, verbose_name='Title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demandproposition',
            name='accepted',
            field=models.BooleanField(default=False, verbose_name='Proposition accepted'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demandproposition',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Additional comments'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demandproposition',
            name='km',
            field=models.IntegerField(blank=True, null=True, verbose_name='Trip distance'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demandproposition',
            name='time',
            field=multiselectfield.db.fields.MultiSelectField(max_length=17, choices=[(1, 'Early morning (8h-10h)'), (2, 'Late morning (10h-12h)'), (3, 'Noon (12h-13h)'), (4, 'Early afternoon (13h-16h)'), (5, 'Late afternoon (16h-19h)'), (6, 'Supper (19h-20h)'), (7, 'Early evening (20h-22h) '), (8, 'Late evening (22h-00h)'), (9, 'Night (00h-8h)')], verbose_name='Hour chosen', help_text='Select the hours that suit you'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='branch',
            field=models.ForeignKey(verbose_name='Branch', to='branch.Branch', related_name='offer_branch'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(max_length=21, choices=[('1', 'Visit home'), ('2', 'Companionship'), ('3', 'Transport by car'), ('4', 'Shopping'), ('5', 'House sitting'), ('6', 'Manual jobs'), ('7', 'Gardening'), ('8', 'Pet sitting'), ('9', 'Personal care'), ('a', 'Administrative'), ('b', 'Other ...')], verbose_name='Type of help'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='donor',
            field=models.ForeignKey(blank=True, related_name='offer_donor', verbose_name='Sender', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='receive_help_from_who',
            field=models.IntegerField(default=5, choices=[(5, 'All'), (3, 'Verified member'), (6, 'My favorite members')], verbose_name='Who can see and respond to demand/offer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='receiver',
            field=models.ForeignKey(blank=True, related_name='offer_receiver', verbose_name='Receiver', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='time',
            field=multiselectfield.db.fields.MultiSelectField(max_length=17, choices=[(1, 'Early morning (8h-10h)'), (2, 'Late morning (10h-12h)'), (3, 'Noon (12h-13h)'), (4, 'Early afternoon (13h-16h)'), (5, 'Late afternoon (16h-19h)'), (6, 'Supper (19h-20h)'), (7, 'Early evening (20h-22h) '), (8, 'Late evening (22h-00h)'), (9, 'Night (00h-8h)')], verbose_name='Busy time', help_text='Select the hours that suit you'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='successdemand',
            name='comment',
            field=models.TextField(verbose_name='Comments'),
            preserve_default=True,
        ),
    ]

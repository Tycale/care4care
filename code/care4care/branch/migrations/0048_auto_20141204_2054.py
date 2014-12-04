# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0047_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='banned',
            field=models.ManyToManyField(verbose_name='Banned members', null=True, blank=True, to=settings.AUTH_USER_MODEL, related_name='banned_users'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='creator',
            field=models.ForeignKey(verbose_name='Branch administrators', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='location',
            field=models.CharField(verbose_name='Address', max_length=256, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='members',
            field=models.ManyToManyField(null=True, related_name='members', verbose_name="Branch's members", blank=True, to=settings.AUTH_USER_MODEL, through='branch.BranchMembers'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(verbose_name="Branch's name", max_length=255),
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
            field=models.ForeignKey(related_name='demand_branch', verbose_name='Branch', to='branch.Branch'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('1', 'Visit home'), ('2', 'Companionship'), ('3', 'Transport by car'), ('4', 'Shopping'), ('5', 'House sitting'), ('6', 'Manual jobs'), ('7', 'Gardening'), ('8', 'Pet sitting'), ('9', 'Personal care'), ('a', 'Administrative'), ('b', 'Other')], verbose_name='Type of help', max_length=21),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='closed',
            field=models.BooleanField(verbose_name='Assigned volunteer', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='donor',
            field=models.ForeignKey(null=True, related_name='demand_donor', verbose_name='Sender', blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='estimated_time',
            field=models.IntegerField(verbose_name='Estimetad time (in minutes)', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='km',
            field=models.IntegerField(verbose_name='Trip distance', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='location',
            field=models.CharField(verbose_name='Address', max_length=256, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='real_time',
            field=models.IntegerField(verbose_name='Real time (int minutes)', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='receive_help_from_who',
            field=models.IntegerField(choices=[(5, 'All'), (3, 'Verified member'), (6, 'My favorite members')], verbose_name='Who can see and respond to demand/offer', default=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='receiver',
            field=models.ForeignKey(null=True, related_name='demand_receiver', verbose_name='Receiver', blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='success',
            field=models.NullBooleanField(verbose_name='Succeded', default=None),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='success_fill',
            field=models.BooleanField(verbose_name='Confirmation request sent', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='time',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Early morning (8h-10h)'), (2, 'Late morning (10h-12h)'), (3, 'Noon (12h-13h)'), (4, 'Early afternoon (13h-16h)'), (5, 'Late afternoon (16h-19h)'), (6, 'Supper (19h-20h)'), (7, 'Early evening (20h-22h) '), (8, 'Late evening (22h-00h)'), (9, 'Night (00h-8h)')], verbose_name='Available times', max_length=17, help_text='Select the hours that suit you'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='title',
            field=models.CharField(verbose_name='Title', max_length=120, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demandproposition',
            name='accepted',
            field=models.BooleanField(verbose_name='Proposition accepted', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demandproposition',
            name='comment',
            field=models.TextField(verbose_name='Additional comments', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demandproposition',
            name='created',
            field=models.DateTimeField(verbose_name='Creation date', auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demandproposition',
            name='km',
            field=models.IntegerField(verbose_name='Trip distance', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demandproposition',
            name='time',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Early morning (8h-10h)'), (2, 'Late morning (10h-12h)'), (3, 'Noon (12h-13h)'), (4, 'Early afternoon (13h-16h)'), (5, 'Late afternoon (16h-19h)'), (6, 'Supper (19h-20h)'), (7, 'Early evening (20h-22h) '), (8, 'Late evening (22h-00h)'), (9, 'Night (00h-8h)')], verbose_name='Hour chosen', max_length=17, help_text='Select the hours that suit you'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='branch',
            field=models.ForeignKey(related_name='offer_branch', verbose_name='Branch', to='branch.Branch'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('1', 'Visit home'), ('2', 'Companionship'), ('3', 'Transport by car'), ('4', 'Shopping'), ('5', 'House sitting'), ('6', 'Manual jobs'), ('7', 'Gardening'), ('8', 'Pet sitting'), ('9', 'Personal care'), ('a', 'Administrative'), ('b', 'Other')], verbose_name='Type of help', max_length=21),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='donor',
            field=models.ForeignKey(null=True, related_name='offer_donor', verbose_name='Sender', blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='receive_help_from_who',
            field=models.IntegerField(choices=[(5, 'All'), (3, 'Verified member'), (6, 'My favorite members')], verbose_name='Who can see and respond to demand/offer', default=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='receiver',
            field=models.ForeignKey(null=True, related_name='offer_receiver', verbose_name='Receiver', blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='time',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Early morning (8h-10h)'), (2, 'Late morning (10h-12h)'), (3, 'Noon (12h-13h)'), (4, 'Early afternoon (13h-16h)'), (5, 'Late afternoon (16h-19h)'), (6, 'Supper (19h-20h)'), (7, 'Early evening (20h-22h) '), (8, 'Late evening (22h-00h)'), (9, 'Night (00h-8h)')], verbose_name='Available times', max_length=17, help_text='Select the hours that suit you'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='successdemand',
            name='comment',
            field=models.TextField(verbose_name='Comments', null=True, blank=True),
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
            field=models.IntegerField(verbose_name='Time spent (in minutes)', null=True, blank=True),
            preserve_default=True,
        ),
    ]

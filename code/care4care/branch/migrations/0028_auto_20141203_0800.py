# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('branch', '0027_auto_20141202_1950'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuccessDemand',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='Comments')),
                ('time', models.IntegerField(verbose_name='Temps passé (en minutes)', null=True, blank=True)),
                ('created', models.DateTimeField(auto_now=True, verbose_name='Date de création')),
                ('ask_to', models.ForeignKey(related_name='success_pending', to=settings.AUTH_USER_MODEL)),
                ('asked_by', models.ForeignKey(related_name='approval_pending', to=settings.AUTH_USER_MODEL)),
                ('branch', models.ForeignKey(related_name='success_branch_pending', to='branch.Branch')),
                ('demand', models.ForeignKey(related_name='success_demand', to='branch.Demand')),
            ],
            options={
                'ordering': ['-created'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='demand',
            options={'ordering': ['date']},
        ),
        migrations.AlterModelOptions(
            name='offer',
            options={'ordering': ['date']},
        ),
        migrations.AddField(
            model_name='demand',
            name='success',
            field=models.NullBooleanField(default=None, verbose_name='Tâche finie avec succès'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='creator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Branch administrators'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='location',
            field=models.CharField(max_length=256, verbose_name='Address', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name="Branch's members", through='branch.BranchMembers', related_name='members', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(help_text="Branch's name", max_length=255, verbose_name="Branch's name"),
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
            field=models.ForeignKey(to='branch.Branch', verbose_name='Branch', related_name='demand_branch'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(max_length=21, choices=[('1', 'Visit home'), ('2', 'Companionship'), ('3', 'Transport by car'), ('4', 'Shopping'), ('5', 'House sitting'), ('6', 'Manuals jobs'), ('7', 'Gardening'), ('8', 'Pet sitting'), ('9', 'Personal care'), ('a', 'Administrative'), ('b', 'Other ...')], verbose_name='Type of help'),
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
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Sender', related_name='demand_donor', null=True),
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
            field=models.CharField(max_length=256, verbose_name='Address', null=True, blank=True),
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
            field=models.IntegerField(default=5, choices=[(5, 'All'), (3, 'Verified member'), (6, 'Favorites')], verbose_name='Who can see and respond to demand/offer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='receiver',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Receiver', related_name='demand_receiver', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='time',
            field=multiselectfield.db.fields.MultiSelectField(help_text='Select the hours that suit you', max_length=17, choices=[(1, 'Early morning (8h-10h)'), (2, 'Late morning (10h-12h)'), (3, 'Noon (12h-13h)'), (4, 'Early afternoon (13h-16h)'), (5, 'Late afternoon (16h-19h)'), (6, 'Supper (19h-20h)'), (7, 'Early evening (20h-22h) '), (8, 'Late evening (22h-00h)'), (9, 'Night (00h-8h)')], verbose_name='Busy time'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='title',
            field=models.CharField(max_length=120, verbose_name='Title', null=True),
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
            field=models.TextField(verbose_name='Additional comments', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demandproposition',
            name='created',
            field=models.DateTimeField(auto_now=True, verbose_name='Date de création'),
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
            field=multiselectfield.db.fields.MultiSelectField(help_text='Select the hours that suit you', max_length=17, choices=[(1, 'Early morning (8h-10h)'), (2, 'Late morning (10h-12h)'), (3, 'Noon (12h-13h)'), (4, 'Early afternoon (13h-16h)'), (5, 'Late afternoon (16h-19h)'), (6, 'Supper (19h-20h)'), (7, 'Early evening (20h-22h) '), (8, 'Late evening (22h-00h)'), (9, 'Night (00h-8h)')], verbose_name='Hour chosen'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='branch',
            field=models.ForeignKey(to='branch.Branch', verbose_name='Branch', related_name='offer_branch'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(max_length=21, choices=[('1', 'Visit home'), ('2', 'Companionship'), ('3', 'Transport by car'), ('4', 'Shopping'), ('5', 'House sitting'), ('6', 'Manuals jobs'), ('7', 'Gardening'), ('8', 'Pet sitting'), ('9', 'Personal care'), ('a', 'Administrative'), ('b', 'Other ...')], verbose_name='Type of help'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='donor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Sender', related_name='offer_donor', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='receive_help_from_who',
            field=models.IntegerField(default=5, choices=[(5, 'All'), (3, 'Verified member'), (6, 'Favorites')], verbose_name='Who can see and respond to demand/offer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='receiver',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Receiver', related_name='offer_receiver', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='time',
            field=multiselectfield.db.fields.MultiSelectField(help_text='Select the hours that suit you', max_length=17, choices=[(1, 'Early morning (8h-10h)'), (2, 'Late morning (10h-12h)'), (3, 'Noon (12h-13h)'), (4, 'Early afternoon (13h-16h)'), (5, 'Late afternoon (16h-19h)'), (6, 'Supper (19h-20h)'), (7, 'Early evening (20h-22h) '), (8, 'Late evening (22h-00h)'), (9, 'Night (00h-8h)')], verbose_name='Busy time'),
            preserve_default=True,
        ),
    ]

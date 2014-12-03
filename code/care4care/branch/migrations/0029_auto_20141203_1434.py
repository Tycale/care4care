# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('branch', '0028_auto_20141203_0800'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='banned',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name='Membres bannis', related_name='banned_users'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=255, verbose_name="Branch's name"),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='donor',
            field=models.ForeignKey(blank=True, null=True, related_name='demand_donor', verbose_name='Sender', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='receive_help_from_who',
            field=models.IntegerField(choices=[(5, 'All'), (3, 'Verified member'), (6, 'Mes membres favoris')], default=5, verbose_name='Who can see and respond to demand/offer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='receiver',
            field=models.ForeignKey(blank=True, null=True, related_name='demand_receiver', verbose_name='Receiver', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='donor',
            field=models.ForeignKey(blank=True, null=True, related_name='offer_donor', verbose_name='Sender', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='receive_help_from_who',
            field=models.IntegerField(choices=[(5, 'All'), (3, 'Verified member'), (6, 'Mes membres favoris')], default=5, verbose_name='Who can see and respond to demand/offer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='receiver',
            field=models.ForeignKey(blank=True, null=True, related_name='offer_receiver', verbose_name='Receiver', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]

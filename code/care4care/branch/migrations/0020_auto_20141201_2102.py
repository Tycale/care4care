# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('branch', '0019_auto_20141201_1201'),
    ]

    operations = [
        migrations.CreateModel(
            name='DemandProposition',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('comment', models.TextField(verbose_name='Commentaire')),
                ('created', models.DateTimeField(auto_now=True, verbose_name="date d'arrivé")),
                ('accepted', models.BooleanField(default=False, verbose_name='Proposition acceptée')),
                ('demand', models.ForeignKey(to='branch.Demand', related_name='propositions')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='propositions')),
            ],
            options={
                'ordering': ['-created'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='demand',
            name='volunteers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='volunteers', blank=True, through='branch.DemandProposition', null=True, verbose_name='Propositions'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='location',
            field=models.CharField(max_length=256, null=True, verbose_name='Address', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=255, help_text='Nom de la localité', verbose_name="Branch's name"),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='location',
            field=models.CharField(max_length=256, null=True, verbose_name='Address', blank=True),
            preserve_default=True,
        ),
    ]

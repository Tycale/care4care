# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0040_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='banned',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, related_name='banned_users', verbose_name='Membres bannis', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='object_id',
            field=models.PositiveIntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='success_fill',
            field=models.BooleanField(default=False, verbose_name='Demande de confirmation envoyée'),
            preserve_default=True,
        ),
    ]

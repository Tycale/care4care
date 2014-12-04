# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0043_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='banned',
            field=models.ManyToManyField(verbose_name='Banned members', null=True, to=settings.AUTH_USER_MODEL, blank=True, related_name='banned_users'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demand',
            name='success_fill',
            field=models.BooleanField(verbose_name='Confirmation request sent', default=False),
            preserve_default=True,
        ),
    ]

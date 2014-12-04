# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0033_auto_20141203_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='banned',
            field=models.ManyToManyField(verbose_name='Banned members', to=settings.AUTH_USER_MODEL, blank=True, null=True, related_name='banned_users'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0035_auto_20141204_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='banned',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, related_name='banned_users', null=True, verbose_name='Banned members'),
            preserve_default=True,
        ),
    ]

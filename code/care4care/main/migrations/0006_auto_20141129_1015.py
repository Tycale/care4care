# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='verifiedinformation',
            options={'ordering': ['date']},
        ),
        migrations.AddField(
            model_name='verifiedinformation',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 11, 29, 10, 15, 29, 899409, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.IntegerField(default=1, choices=[(1, 'Actif'), (2, 'En vacances'), (3, 'Désactivé')]),
            preserve_default=True,
        ),
    ]

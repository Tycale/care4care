# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0006_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='receive_help_from_who',
            field=models.IntegerField(choices=[(5, 'Tous'), (3, 'Membre vérifié'), (6, 'Favoris (inclus le réseau personnel)')], verbose_name='Qui peut voir et répondre à la demande/offre ?', default=5),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0007_job_receive_help_from_who'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='state',
            field=models.IntegerField(choices=[(1, 'créé'), (2, 'reçu proposition'), (3, 'proposition acceptée'), (4, 'completé'), (5, 'echoué')], default=1, verbose_name='Status'),
            preserve_default=True,
        ),
    ]

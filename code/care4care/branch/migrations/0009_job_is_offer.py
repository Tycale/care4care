# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0008_job_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='is_offer',
            field=models.BooleanField(verbose_name='Est-ce une offre ?', default=False),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_squashed_0020_auto_20141201_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(default=1, choices=[(1, 'Membre'), (2, 'Non-membre'), (3, 'Membre vérifié')], help_text="Un member pourra aider ou être aidé alors qu'un                                         non-membre est un professionnel qui s'inscrira pour avoir accès aux données d'un                                         patient. Veuillez choisir celui qui vous correspond", verbose_name='Type de compte'),
            preserve_default=True,
        ),
    ]

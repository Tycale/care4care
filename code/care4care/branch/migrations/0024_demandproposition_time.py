# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0023_auto_20141201_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='demandproposition',
            name='time',
            field=multiselectfield.db.fields.MultiSelectField(help_text='Selectionnez les heures qui vous conviennent', verbose_name='Heure(s) choisie(s)', default=['1'], max_length=17, choices=[(1, 'Début de matinée (8h-10h)'), (2, 'Fin de matinée (10h-12h)'), (3, 'Midi (12h-13h)'), (4, "Début d'après-midi (13h-16h)"), (5, "Fin d'après-midi (16h-19h)"), (6, 'Repas du soir (19h-20h)'), (7, 'Début de soirée (20h-22h)'), (8, 'Fin de soirée (22h-00h)'), (9, 'Nuit (00h-8h)')]),
            preserve_default=False,
        ),
    ]

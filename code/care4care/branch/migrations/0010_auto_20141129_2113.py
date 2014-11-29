# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0009_job_is_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(verbose_name="Type d'aide", max_length=26, choices=[(1, 'Visite à la maison'), (2, 'Tenir compagnie'), (3, 'Transport par voiture'), (4, 'Shopping'), (5, 'Garder des maisons'), (6, 'Petits boulots manuels'), (7, 'Jardinage'), (8, 'Garder des animaux'), (9, 'Soins personnels'), (10, 'Administratif'), (11, 'Autre'), (12, 'Spécial ... :D')]),
            preserve_default=True,
        ),
    ]

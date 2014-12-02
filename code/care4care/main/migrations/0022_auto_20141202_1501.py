# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20141201_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(default=1, verbose_name='Type de compte', help_text="Un member pourra aider ou être aidé alors qu'un                                         non-membre est un professionnel qui s'inscrira pour avoir accès aux données d'un                                         patient. Veuillez choisir celui qui vous correspond", choices=[(1, 'Membre'), (2, 'Non-membre')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='asked_job',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, verbose_name='Quelles sont les tâches dont vous avez besoin ?', max_length=21, choices=[(1, 'Visite à la maison'), (2, 'Tenir compagnie'), (3, 'Transport par voiture'), (4, 'Shopping'), (5, 'Garder des maisons'), (6, 'Petits boulots manuels'), (7, 'Jardinage'), (8, 'Garder des animaux'), (9, 'Soins personnels'), ('a', 'Administratif'), ('b', 'Autre')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='offered_job',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, verbose_name='Quelles sont les tâches que vous souhaitez effectuer ?', max_length=21, choices=[(1, 'Visite à la maison'), (2, 'Tenir compagnie'), (3, 'Transport par voiture'), (4, 'Shopping'), (5, 'Garder des maisons'), (6, 'Petits boulots manuels'), (7, 'Jardinage'), (8, 'Garder des animaux'), (9, 'Soins personnels'), ('a', 'Administratif'), ('b', 'Autre')]),
            preserve_default=True,
        ),
    ]

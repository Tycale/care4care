# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_auto_20141204_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='how_found',
            field=multiselectfield.db.fields.MultiSelectField(max_length=41, choices=[('internet', 'The Internet'), ('show', 'A presentation, brochure, flyer,... '), ('branch', 'The local branch'), ('member', 'Another member'), ('friends', 'Friends or family'), ('other', 'Other')], verbose_name='How did you hear about care4care ?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='offered_job',
            field=multiselectfield.db.fields.MultiSelectField(max_length=21, blank=True, choices=[('1', 'Visit home'), ('2', 'Companionship'), ('3', 'Transport by car'), ('4', 'Shopping'), ('5', 'House sitting'), ('6', 'Manual jobs'), ('7', 'Gardening'), ('8', 'Pet sitting'), ('9', 'Personal care'), ('a', 'Administrative'), ('b', 'Other')], verbose_name='What jobs you want to do?'),
            preserve_default=True,
        ),
    ]

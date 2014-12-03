# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_auto_20141203_0800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(choices=[(1, 'Member'), (2, 'Non-member'), (3, 'Verified member')], default=1, help_text='A member can help or be helped while a non-member is a professional who registers to access patient data. Please choose the one that suits you', verbose_name='Account type'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='receive_help_from_who',
            field=models.IntegerField(choices=[(5, 'All'), (3, 'Verified member'), (6, 'Mes membres favoris')], default=5, verbose_name='Receive offers and demands'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='photos/', default='photos/tinder_match.jpg'),
            preserve_default=True,
        ),
    ]

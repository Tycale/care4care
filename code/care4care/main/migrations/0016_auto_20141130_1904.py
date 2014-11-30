# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20141129_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='first_name',
            field=models.CharField(verbose_name='First name', max_length=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')], blank=True, verbose_name='Spoken languages', max_length=8),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='last_name',
            field=models.CharField(verbose_name='Name', max_length=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='location',
            field=models.CharField(max_length=256, blank=True, verbose_name='Address', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='first_name',
            field=models.CharField(verbose_name='First name', max_length=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')], blank=True, verbose_name='Spoken languages', max_length=8),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='last_name',
            field=models.CharField(verbose_name='Name', max_length=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='location',
            field=models.CharField(max_length=256, blank=True, verbose_name='Address', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(verbose_name='First name', max_length=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('fr', 'French'), ('en', 'English'), ('nl', 'Dutch')], blank=True, verbose_name='Spoken languages', max_length=8),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(verbose_name='Name', max_length=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.CharField(max_length=256, blank=True, verbose_name='Address', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='photos/', default='photos/default_avatar.png'),
            preserve_default=True,
        ),
    ]

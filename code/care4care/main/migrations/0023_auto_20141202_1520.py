# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re
import django.core.validators
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_auto_20141202_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='comments',
            field=models.CharField(max_length=255, blank=True, verbose_name='Additional comments'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=75, blank=True, verbose_name='Email address'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='mobile_number',
            field=models.CharField(max_length=16, blank=True, verbose_name='Phone number (mobile)', validators=[django.core.validators.RegexValidator(message="Your phone number must be in format '+99999999'. Up to 15 digits.", regex='^\\+?1?\\d{9,15}$')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone_number',
            field=models.CharField(max_length=16, blank=True, verbose_name='Phone number (home)', validators=[django.core.validators.RegexValidator(message="Your phone number must be in format '+99999999'. Up to 15 digits.", regex='^\\+?1?\\d{9,15}$')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='relationship',
            field=models.CharField(max_length=255, blank=True, verbose_name='Your relationship with that person'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='mobile_number',
            field=models.CharField(max_length=16, blank=True, verbose_name='Phone number (mobile)', validators=[django.core.validators.RegexValidator(message="Your phone number must be in format '+99999999'. Up to 15 digits.", regex='^\\+?1?\\d{9,15}$')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='order',
            field=models.IntegerField(default=0, choices=[(1, 'First contact'), (2, 'Contact'), (3, 'Last contact')], verbose_name='Priority'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='phone_number',
            field=models.CharField(max_length=16, blank=True, verbose_name='Phone number (home)', validators=[django.core.validators.RegexValidator(message="Your phone number must be in format '+99999999'. Up to 15 digits.", regex='^\\+?1?\\d{9,15}$')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Birthday'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='credit',
            field=models.IntegerField(default=0, verbose_name='Remaining credit'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=75, verbose_name='Email address'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='how_found',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('internet', 'The Internet'), ('show', 'A presentation, brochure, flyer,... '), ('branch', 'The local branch'), ('member', 'Another member'), ('friends', 'Friends or family'), ('other', 'Other ...')], max_length=41, verbose_name='How did you hear about care4care ?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile_number',
            field=models.CharField(max_length=16, blank=True, verbose_name='Phone number (mobile)', validators=[django.core.validators.RegexValidator(message="Your phone number must be in format '+99999999'. Up to 15 digits.", regex='^\\+?1?\\d{9,15}$')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=16, blank=True, verbose_name='Phone number (home)', validators=[django.core.validators.RegexValidator(message="Your phone number must be in format '+99999999'. Up to 15 digits.", regex='^\\+?1?\\d{9,15}$')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.IntegerField(default=1, choices=[(1, 'Active'), (2, 'On vacation'), (3, 'Disabled')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(default=1, choices=[(1, 'Member'), (2, 'Non-member')], help_text='A member can help or be helped while a non-member is a professional who registers to access patient data. Please choose the one that suits you', verbose_name='Account type'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, unique=True, verbose_name='Username', validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), 'Enter a valid username. No more than 30 characters. There may be numbers andcharacters  @/./+/-/_', 'invalid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifiedinformation',
            name='criminal_record',
            field=models.FileField(upload_to='documents/', null=True, verbose_name='Criminal record'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifiedinformation',
            name='recomendation_letter_1',
            field=models.FileField(upload_to='documents/', null=True, verbose_name='Letter of recommendation n°1'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifiedinformation',
            name='recomendation_letter_2',
            field=models.FileField(upload_to='documents/', null=True, verbose_name='Letter de recommendation n°2'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='additional_info',
            field=models.TextField(max_length=300, blank=True, verbose_name='Additional information'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='asked_job',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Visit home'), (2, 'Companionship'), (3, 'Transport by car'), (4, 'Shopping'), (5, 'House sitting'), (6, 'Manuals jobs'), (7, 'Gardening'), (8, 'Pet sitting'), (9, 'Personal care'), ('a', 'Administrative'), ('b', 'Other ...')], blank=True, max_length=21, verbose_name='What jobs you need?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='can_wheelchair',
            field=models.BooleanField(default=False, choices=[(True, 'Yes'), (False, 'No')], verbose_name='Can you carry a wheelchair in your car?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='drive_license',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Moped'), (2, 'Motorcycle'), (3, 'Car'), (4, 'Truck'), (5, 'Bus'), (6, 'Tractor')], blank=True, max_length=11, verbose_name='Type of driving license'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='have_car',
            field=models.BooleanField(default=False, choices=[(True, 'Yes'), (False, 'No')], verbose_name='Do you have a car?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='hobbies',
            field=models.TextField(max_length=200, blank=True, verbose_name='Your hobby'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='mail_preferences',
            field=models.IntegerField(default=1, choices=[(1, 'Message box'), (2, 'Mail')], verbose_name='Receive my messages'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='offered_job',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Visit home'), (2, 'Companionship'), (3, 'Transport by car'), (4, 'Shopping'), (5, 'House sitting'), (6, 'Manuals jobs'), (7, 'Gardening'), (8, 'Pet sitting'), (9, 'Personal care'), ('a', 'Administrative'), ('b', 'Other ...')], blank=True, max_length=21, verbose_name='What jobs you want to do?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verifieduser',
            name='receive_help_from_who',
            field=models.IntegerField(default=5, choices=[(5, 'All'), (3, 'Verified member'), (6, 'Favorites')], verbose_name='Receive offers and demands'),
            preserve_default=True,
        ),
    ]

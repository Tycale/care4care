#-*- coding: utf-8 -*-
from django import forms
from news.models import News
from bootstrap3_datetime.widgets import DateTimePicker


import time

class NewsForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = News
        exclude = ('date_creation','date_fin', 'visible', 'auteur', 'slug')
        dateTimeOptions = {
        'format': 'DD/MM/YYYY HH:mm',
        'autoclose': True,
        'showMeridian' : True,
        "pickTime": True
        }
        widgets =  {'date_debut' : DateTimePicker(options=dateTimeOptions),}

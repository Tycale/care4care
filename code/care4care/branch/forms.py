from django import forms
from django.utils.translation import ugettext as _
from bootstrap3_datetime.widgets import DateTimePicker
from multiselectfield import MultiSelectField

from branch.models import Branch, Job

from django.utils import timezone

from branch.widgets import OneJobSelect

class CreateBranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'location', 'latitude', 'longitude']
        widgets = {
            'latitude': forms.HiddenInput,
            'longitude': forms.HiddenInput,
            'location': forms.HiddenInput,
        }

class ChooseBranchForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput)

    def clean(self):
        id = self.cleaned_data.get('id')
        try:
            Branch.objects.get(pk=id)
        except Branch.DoesNotExist:
            raise forms.ValidationError(_("Veuillez choisir un point sur la carte"))
        super(ChooseBranchForm, self).clean()

    class Meta:
        fields = ['id']

class NeedHelpForm(forms.ModelForm):
    category = MultiSelectField(verbose_name=_("Categorie"))

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < timezone.now():
            raise forms.ValidationError(_("Veuillez choisir une date dans le futur."))
        return date

    def clean_estimated_time(self):
        est = self.cleaned_data.get('estimated_time')
        if est <= 0:
            raise forms.ValidationError(_("Le temps estimé doit être plus grand que 0 minute."))
        return est

    class Meta:
        model = Job
        fields = ['description', 'estimated_time', 'category', 'date', 'time', 'location', 'latitude', 'longitude', 'title', 'receive_help_from_who']
        widgets = {
            'latitude': forms.HiddenInput,
            'longitude': forms.HiddenInput,
            'location': forms.HiddenInput,
            'date': DateTimePicker(options={"pickTime": False,}),
            'category': OneJobSelect,
        }

class OfferHelpForm(forms.ModelForm):
    category = MultiSelectField(verbose_name=_("Categorie"))

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < timezone.now():
            raise forms.ValidationError(_("Veuillez choisir une date dans le futur."))
        return date

    class Meta:
        model = Job
        fields = ['category', 'date', 'time', 'receive_help_from_who',]
        widgets = {
            'latitude': forms.HiddenInput,
            'longitude': forms.HiddenInput,
            'location': forms.HiddenInput,
            'date' : DateTimePicker(options={"pickTime": False,}),
        }

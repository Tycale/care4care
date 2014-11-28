from django import forms
from django.utils.translation import ugettext as _
from bootstrap3_datetime.widgets import DateTimePicker
from multiselectfield import MultiSelectField

from branch.models import Branch, Job

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

    category =  MultiSelectField(verbose_name=_("Categorie"))

    class Meta:
        model = Job
        fields = ['description', 'estimated_time', 'category', 'date', 'time', 'location', 'latitude', 'longitude', 'title']
        widgets = {
            'latitude': forms.HiddenInput,
            'longitude': forms.HiddenInput,
            'location': forms.HiddenInput,
            'date' : DateTimePicker(options={"format": "DD/MM/YYYY", "pickTime": False, 'language': 'fr'}),
        }
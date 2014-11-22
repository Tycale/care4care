from django import forms
#from django.utils.translation import ugettext as _

from branch.models import Branch

class CreateBranchForm(forms.ModelForm):
	class Meta:
		model = Branch
		fields = ['name', 'location', 'latitude', 'longitude']
		widgets = {
            'latitude': forms.HiddenInput,
            'longitude': forms.HiddenInput,
            'location': forms.HiddenInput,
        }
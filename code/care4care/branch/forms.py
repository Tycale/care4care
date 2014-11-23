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

class ChooseBranchForm(forms.Form):
	id = forms.IntegerField(widget=forms.HiddenInput)

	def clean(self):
		id = self.cleaned_data.get('id')
		try:
			Branch.objects.get(pk=id)
		except Branch.DoesNotExist:
			raise forms.ValidationError("Veuillez choisir un point sur la carte")
		super(ChooseBranchForm, self).clean()

	class Meta:
		fields = ['id']

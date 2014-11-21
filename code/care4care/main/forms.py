from django import forms
from django.utils.translation import ugettext_lazy as _
from main.models import User, VerifiedInformation
from multiselectfield import MultiSelectField

from django.forms.extras import SelectDateWidget
import datetime

class CareRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label=_("Prénom"),)
    last_name = forms.CharField(label=_("Nom de famille"),)
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Mot de passe"))
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Mot de passe (à nouveau)"))

    birth_date = forms.DateField(label=_("Date de naissance (DD/MM/YYYY)"),
                                 widget=SelectDateWidget(years=range(datetime.date.today().year-100, \
                                                                     datetime.date.today().year)),
                                 initial=datetime.date.today())
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'languages', \
         'how_found', 'birth_date', 'phone_number', 'mobile_number', 'location', 'latitude', 'longitude','user_type']
        widgets = {
            'latitude': forms.HiddenInput,
            'longitude': forms.HiddenInput,
            'location': forms.HiddenInput,
        }

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        UserModel = self._meta.model
        username = self.cleaned_data["username"].lower()
        try:
            UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return username
        raise forms.ValidationError(_("Cet utilisateur existe déjà dans notre système. Veuillez utiliser utiliser le formulaire 'Mot de passe perdu' si vous êtes déjà enregistré."))

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        """
        print(self.cleaned_data)
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("Les mots de passe ne sont pas identiques."))
        if not 'longitude' in self.cleaned_data or not self.cleaned_data['longitude']:
            raise forms.ValidationError(_("Veuillez introduire une adresse valide via les propositions."))
        if not 'latitude' in self.cleaned_data or not self.cleaned_data['latitude']:
            raise forms.ValidationError(_("Veuillez introduire une adresse valide via les propositions."))

        return self.cleaned_data

class ProfileManagementForm(forms.ModelForm):

    favorites = MultiSelectField(verbose_name="Vos membres favoris", help_text="test")
    personal_network = MultiSelectField(verbose_name="Votre reseau")
    
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'status', 'languages', 'location', 'mail_preferences', 'preferred_job',
        'receive_help_from_who', 'favorites', 'personal_network']

class VerifiedInformationForm(forms.ModelForm):
    class Meta:
        model = VerifiedInformation
        fields = ['recomendation_letter_1', 'recomendation_letter_2', 'criminal_record']


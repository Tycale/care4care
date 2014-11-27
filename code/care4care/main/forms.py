from django import forms
from django.utils.translation import ugettext as _
from main.models import User, VerifiedInformation, EmergencyContact
from branch.models import Job
from multiselectfield import MultiSelectField

from django.forms.extras import SelectDateWidget
import datetime

from branch.models import Branch

from django.template.defaultfilters import filesizeformat

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
    id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', \
         'how_found', 'birth_date', 'phone_number', 'mobile_number', 'user_type']


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
        cleaned_data = super(CareRegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("Les mots de passe ne sont pas identiques."))

        id = self.cleaned_data.get('id')

        try:
            Branch.objects.get(pk=id)
        except Branch.DoesNotExist:
            raise forms.ValidationError("Veuillez choisir une branche en choisissant un marqueur rouge sur la carte")
        
        if id == -1:
            raise forms.ValidationError("Veuillez choisir une branche en choisissant un marqueur rouge sur la carte")

        return self.cleaned_data

class ProfileManagementForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'status', 'languages', 'location', 'mail_preferences', 'asked_job', 'offered_job', \
            'latitude', 'longitude', 'facebook', 'additional_info', 'have_car', \
            'can_wheelchair', 'drive_license', 'hobbies', ]
        widgets = {
            'latitude': forms.HiddenInput,
            'longitude': forms.HiddenInput,
            'location': forms.HiddenInput,
            'have_car': forms.RadioSelect,
            'can_wheelchair': forms.RadioSelect,
        }

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        """
        cleaned_data = super(ProfileManagementForm, self).clean()
        if not 'longitude' in self.cleaned_data or not self.cleaned_data['longitude']:
            raise forms.ValidationError(_("Veuillez introduire une adresse valide via les propositions."))
        if not 'latitude' in self.cleaned_data or not self.cleaned_data['latitude']:
            raise forms.ValidationError(_("Veuillez introduire une adresse valide via les propositions."))

        return self.cleaned_data

class ContentTypeRestrictedFileField(forms.FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types.
        Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file
        size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    """
    def __init__(self, content_types=None, max_upload_size=5242880, *args, **kwargs):
        self.content_types = content_types
        self.max_upload_size = max_upload_size

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)
        file = data.file
        try:
            content_type = file.content_type
            if content_type in self.content_types or content_types == None:
                if file._size > self.max_upload_size:
                    raise forms.ValidationError(_('Votre fichier doit peser moins de '
                                                '%s. Taille actuelle %s')
                                                % (filesizeformat(self.max_upload_size), filesizeformat(file._size)))
            else:
                raise forms.ValidationError(_('Type de fichier non supporté'))
        except AttributeError:
            pass

        return data

class VerifiedInformationForm(forms.ModelForm):
    recomendation_letter_1 = ContentTypeRestrictedFileField(content_types=['application/pdf'], max_upload_size=5242880)
    recomendation_letter_2 = ContentTypeRestrictedFileField(content_types=['application/pdf'], max_upload_size=5242880)
    criminal_record = ContentTypeRestrictedFileField(content_types=['application/pdf'], max_upload_size=5242880)

    class Meta:
        model = VerifiedInformation
        fields = ['recomendation_letter_1', 'recomendation_letter_2', 'criminal_record']


class EmergencyContactCreateForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        exclude = ['user']

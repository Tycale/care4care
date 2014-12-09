from django import forms
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as __
from django.utils import timezone
from main.models import User, VerifiedInformation, EmergencyContact, JobType, MemberType, GIVINGTO
from branch.models import Job, Branch, JobCategory, TIME_CHOICES
from multiselectfield import MultiSelectField
from bootstrap3_datetime.widgets import DateTimePicker
from ajax_select.fields import AutoCompleteWidget
from django.forms.extras import SelectDateWidget
import datetime

from django.template.defaultfilters import filesizeformat

class CareRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label=__("Prénom"),)
    last_name = forms.CharField(label=__("Nom de famille"),)
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=__("Mot de passe"))
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=__("Mot de passe (à nouveau)"))

    birth_date = forms.DateField(label=__("Date de naissance"),
                                 widget=SelectDateWidget(years=range(datetime.date.today().year-100, \
                                                                     datetime.date.today().year)),
                                 initial=datetime.date.today())
    id = forms.IntegerField(widget=forms.HiddenInput)
    user_type = forms.ChoiceField(label=__("Type de compte"), choices = MemberType.MEMBER_TYPES[:-1])

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
        id_user_type = self.cleaned_data.get('user_type')

        # si c'est un user de type membre verifier qu'il a une branche
        # sinon ne rien faire
        if int(id_user_type) == MemberType.MEMBER:
            try:
                Branch.objects.get(pk=id)
            except Branch.DoesNotExist:
                raise forms.ValidationError(_("Veuillez choisir une branche en choisissant un marqueur rouge sur la carte"))

            if id == -1:
                raise forms.ValidationError(_("Veuillez choisir une branche en choisissant un marqueur rouge sur la carte"))

        return self.cleaned_data

class ProfileManagementForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone_number','mobile_number', 'status', 'languages', 'location', 'offered_job', \
            'latitude', 'longitude', 'facebook', 'additional_info', 'have_car', \
            'can_wheelchair', 'drive_license', 'hobbies', 'photo', 'receive_help_from_who']
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
        """
        Pas obligé de mettre l'adresse
        """
        return self.cleaned_data

class NonProfileManagementForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['organization', 'work']

class VerifiedProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'mobile_number', 'status', 'languages', 'location', 'mail_preferences', 'offered_job', \
            'latitude', 'longitude', 'facebook', 'additional_info', 'have_car', \
            'can_wheelchair', 'drive_license', 'hobbies', 'photo', 'receive_help_from_who']
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
        cleaned_data = super(VerifiedProfileForm, self).clean()
        if not 'longitude' in self.cleaned_data or not self.cleaned_data['longitude']:
            raise forms.ValidationError(_("Veuillez introduire une adresse valide via les propositions."))
        if not 'latitude' in self.cleaned_data or not self.cleaned_data['latitude']:
            raise forms.ValidationError(_("Veuillez introduire une adresse valide via les propositions."))
        if not 'email' in self.cleaned_data or not self.cleaned_data['email']:
            raise forms.ValidationError(_("Veuillez introduire une adresse e-mail valide via les propositions."))
        if not 'latitude' in self.cleaned_data or not self.cleaned_data['latitude']:
            raise forms.ValidationError(_("Veuillez introduire une adresse valide via les propositions."))
        if ((not 'mobile_number' in self.cleaned_data or not self.cleaned_data['mobile_number']) and (not 'phone_number' in self.cleaned_data or not self.cleaned_data['phone_number'])):
            raise forms.ValidationError(_("Veuillez introduire au moins un numéro de téléphone (mobile ou fixe)."))
        if (len('languages')==0) or not self.cleaned_data['languages']:
            raise forms.ValidationError(_("Veuillez introduire une langue."))

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
                                                '{maxsize}. Taille actuelle {currentsize}').format(maxsize=self.max_upload_size, currentsize=file._size))
        
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
        exclude = ['user', 'latitude', 'longitude']

class JobSearchForm(forms.Form):
    job_type =  forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=JobType.JOB_TYPES, label = __("Type de job (rien = tout)"))
    category = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=JobCategory.JOB_CATEGORIES, label = __("Catégorie du job (rien = tout)"))
    date1 = forms.DateTimeField(required=False, label =__("A partir du"),widget=DateTimePicker(options={"pickTime": False,}))
    date2 = forms.DateTimeField(required=False, label =__("Jusqu'au"),widget=DateTimePicker(options={"pickTime": False,}))
    receive_help_from_who = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=MemberType.MEMBER_TYPES_GROUP, label = __("Qui peut fournir son aide ?"))
    time = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=TIME_CHOICES, label = __("A quelle heure ?"))

    def clean(self):
        cleaned_data = super(JobSearchForm, self).clean()

        if self.cleaned_data['date1']:
            if self.cleaned_data['date1']<timezone.now()-timezone.timedelta(hours=24):
                raise forms.ValidationError(_("Incohérence dans les dates."))
            if self.cleaned_data['date2'] and self.cleaned_data['date2'] < self.cleaned_data['date1']:
                raise forms.ValidationError(_("Incohérence dans les dates."))
        elif self.cleaned_data['date2']:
            if self.cleaned_data['date2']<timezone.now()-timezone.timedelta(hours=24):
                raise forms.ValidationError(_("Incohérence dans les dates."))


class GiftForm(forms.Form):
    check = forms.ChoiceField(label = __("Donner à:"),widget=forms.RadioSelect, choices=GIVINGTO, initial=1)
    user = forms.CharField(required=False, label = __("Username"), widget=AutoCompleteWidget('user'))
    amount = forms.IntegerField(label = __("Montant du temps (plus que 1)"), min_value=1, initial=60)
    message = forms.CharField(required=False, widget=forms.Textarea, label = __("Message"))

    def __init__(self, *args, **kwargs):
        self.ruser = kwargs.pop('ruser')
        super(GiftForm, self).__init__(*args, **kwargs)

    def clean_user(self):
        print(self.cleaned_data)
        cleaned_data = super(GiftForm, self).clean()
        if self.cleaned_data['check']=='1':
            if self.cleaned_data['user']=="":
                raise forms.ValidationError(_("Indiquez un utilisateur."))     
        
            try:
                a = User.objects.get(username=self.cleaned_data['user'])
            except Exception:
                raise forms.ValidationError(_("Indiquez un utilisateur existant."))
        
            if a.id == self.ruser.id:
                raise forms.ValidationError(_("Vous ne pouvez pas donner à vous même."))
        return cleaned_data['user']

    def clean_amount(self):
        cleaned_data = super(GiftForm, self).clean()
        if self.cleaned_data['amount'] > self.ruser.credit:
            raise forms.ValidationError(_("Vous ne pouvez pas donner plus d'heure que ce que vous avez."))
        return cleaned_data['amount']


class AddUser(forms.Form):
    user = forms.CharField(label=__("Username"), widget=AutoCompleteWidget('user'))

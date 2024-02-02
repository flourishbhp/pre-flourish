from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from ..models import PreFlourishClinicianNotes, ClinicianNotesImage


class PreflourishClinicianNotesForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm,):
    class Meta:
        model = PreFlourishClinicianNotes
        fields = '__all__'


class PreflourishClinicianNotesImageForm(forms.ModelForm):
    class Meta:
        model = ClinicianNotesImage
        fields = '__all__'

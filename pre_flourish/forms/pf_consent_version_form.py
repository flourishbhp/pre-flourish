from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import PFConsentVersion


class PFConsentVersionForm(SiteModelFormMixin, FormValidatorMixin,
                           forms.ModelForm):
    class Meta:
        model = PFConsentVersion
        fields = '__all__'

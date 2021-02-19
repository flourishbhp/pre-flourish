from django import forms
from django.conf import settings

from edc_form_validators import FormValidatorMixin
from edc_base.sites import SiteModelFormMixin

from ...models import CaregiverChildScreeningConsent



class CaregiverChildScreeningConsentForm(SiteModelFormMixin, FormValidatorMixin,
                                         forms.ModelForm):


    class Meta:
        model = CaregiverChildScreeningConsent
        fields = '__all__'

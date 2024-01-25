from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ...form_validators import PreFlourishCaregiverChildConsentFormValidator
from ...models import PreFlourishCaregiverChildConsent


class PreFlourishCaregiverChildConsentForm(
    SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):
    form_validator_cls = PreFlourishCaregiverChildConsentFormValidator

    def has_changed(self):
        return True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = getattr(self, 'instance', None)
        subject_identifier = instance.subject_identifier if instance else None
        if subject_identifier:
            for key in self.fields.keys():
                self.fields[key].disabled = True

    class Meta:
        model = PreFlourishCaregiverChildConsent
        fields = '__all__'

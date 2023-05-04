from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ...form_validators import HuuPreEnrollmentFormValidator
from ...models import PreFlourishCaregiverChildConsent


class PreFlourishCaregiverChildConsentForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    # form_validator_cls = HuuPreEnrollmentFormValidator
    def has_changed(self):
        return True

    class Meta:
        model = PreFlourishCaregiverChildConsent
        fields = '__all__'

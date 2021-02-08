from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ...form_validators import HuuPreEnrollmentFormValidator
from ...models import HuuPreEnrollment


class HuuPreEnrollmentForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = HuuPreEnrollmentFormValidator

    class Meta:
        model = HuuPreEnrollment
        fields = '__all__'

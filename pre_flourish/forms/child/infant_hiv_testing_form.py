from django import forms
from edc_form_validators import FormValidatorMixin

from flourish_child_validations.form_validators import InfantHIVTestingFormValidator
from ...models import PFInfantHIVTesting


class InfantHIVTestingForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = InfantHIVTestingFormValidator

    class Meta:
        model = PFInfantHIVTesting
        fields = '__all__'

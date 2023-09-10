from django import forms
from edc_form_validators import FormValidatorMixin

from flourish_child_validations.form_validators import ChildPregTestingFormValidator
from ...models import PFChildPregTesting


class ChildPregTestingForm(FormValidatorMixin, forms.ModelForm):
    #form_validator_cls = ChildPregTestingFormValidator

    class Meta:
        model = PFChildPregTesting
        fields = '__all__'

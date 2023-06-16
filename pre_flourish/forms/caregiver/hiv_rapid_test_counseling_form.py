from django import forms
from edc_form_validators import FormValidatorMixin

from flourish_child_validations.form_validators import ChildHIVRapidTestValidator
from pre_flourish.models import PFHIVRapidTestCounseling


class PFHIVRapidTestCounselingForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = ChildHIVRapidTestValidator

    class Meta:
        model = PFHIVRapidTestCounseling
        fields = '__all__'

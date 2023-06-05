from django import forms
from edc_form_validators import FormValidatorMixin

from flourish_child_validations.form_validators import ChildHIVRapidTestValidator
from pre_flourish.models import PFChildHIVRapidTestCounseling


class PFChildHIVRapidTestCounselingForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = ChildHIVRapidTestValidator

    class Meta:
        model = PFChildHIVRapidTestCounseling
        fields = '__all__'

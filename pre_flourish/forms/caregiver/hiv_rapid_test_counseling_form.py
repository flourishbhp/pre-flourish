from django import forms
from edc_form_validators import FormValidatorMixin

from pre_flourish.form_validators import PFChildHIVRapidTestValidator
from pre_flourish.models import PFHIVRapidTestCounseling


class PFHIVRapidTestCounselingForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = PFChildHIVRapidTestValidator

    class Meta:
        model = PFHIVRapidTestCounseling
        fields = '__all__'

from django import forms
from edc_form_validators import FormValidatorMixin

from pre_flourish.models import PFChildHIVRapidTestCounseling
from ...form_validators import PFChildHIVRapidTestValidator

class PFChildHIVRapidTestCounselingForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = PFChildHIVRapidTestValidator

    class Meta:
        model = PFChildHIVRapidTestCounseling
        fields = '__all__'

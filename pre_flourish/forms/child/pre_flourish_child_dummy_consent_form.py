from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from ...models import PreFlourishChildDummySubjectConsent
from ...form_validators import PreFlourishChildAssentFormValidator

class PreFlourishChildDummySubjectConsentForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):
    
    #form_validator_cls = PreFlourishChildAssentFormValidator

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        #widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)
    
    class Meta:
        model = PreFlourishChildDummySubjectConsent
        fields = '__all__'
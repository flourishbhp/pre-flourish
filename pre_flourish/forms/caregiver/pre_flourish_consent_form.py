from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
# from flourish_form_validations.form_validators import SubjectConsentFormValidator
from ...models import PreFlourishConsent


class PreFlourishConsentForm(SiteModelFormMixin, FormValidatorMixin,
                             forms.ModelForm):

    # form_validator_cls = SubjectConsentFormValidator
    #
    # form_validator_cls.subject_consent_model = 'pre_flourish.preflourishconsent'
    #
    # form_validator_cls.caregiver_locator_model = None

    screening_identifier = forms.CharField(
        label='Screening Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    subject_identifier = forms.CharField(
        label='Pre Flourish Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    class Meta:
        model = PreFlourishConsent
        fields = '__all__'

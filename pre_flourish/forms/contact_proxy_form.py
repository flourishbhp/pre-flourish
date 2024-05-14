from django import forms
from edc_form_validators import FormValidatorMixin
from flourish_follow.form_validations import FUContactFormValidator

from ..models.contact_proxy import PreFlourishContact


class PreFlourishContactForm(FormValidatorMixin, forms.ModelForm):

    form_validator_cls = FUContactFormValidator

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    
    class Meta:
        model = PreFlourishContact
        fields = '__all__'

from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from flourish_follow.form_validations import LogEntryFormValidator

from ...models import PreFlourishLogEntry


class PreFlourishLogEntryForm(
    SiteModelFormMixin, FormValidatorMixin,
    forms.ModelForm):
    form_validator_cls = LogEntryFormValidator

    study_maternal_identifier = forms.CharField(
        label='Study maternal Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    prev_study = forms.CharField(
        label=' Previous Study Name',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    phone_num_type = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label='Which phone number(s) was used for contact?')

    phone_num_success = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label='Which number(s) were you successful in reaching?')

    class Meta:
        model = PreFlourishLogEntry
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        # choices = self.custom_choices
        # self.fields['phone_num_type'].choices = choices
        # self.fields['phone_num_success'].choices = choices + (('none_of_the_above', 'None of the above'),)

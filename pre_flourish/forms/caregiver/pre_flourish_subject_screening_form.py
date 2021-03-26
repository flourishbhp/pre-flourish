from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ...models import PreFlourishSubjectScreening


class PreFlourishSubjectScreeningForm(SiteModelFormMixin, FormValidatorMixin,
                                      forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        age_in_years = cleaned_data.get('age_in_years')
        if age_in_years < 18:
            message = {'age_in_years':
                       'Participant is less than 18 years, age derived '
                       f'from the DOB is {age_in_years}'}
            raise forms.ValidationError(message)
        return cleaned_data

    screening_identifier = forms.CharField(
        required=False,
        label='Screening Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = PreFlourishSubjectScreening
        fields = '__all__'

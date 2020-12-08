from django import forms
from edc_form_validators import FormValidatorMixin

from ...models import PreFlourishOffStudy


class PreFlourishOffStudyForm(FormValidatorMixin, forms.ModelForm):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get('subject_identifier')

        super().clean()
        self.validate_against_consent_datetime(
            self.cleaned_data.get('report_datetime'))

    class Meta:
        model = PreFlourishOffStudy
        fields = '__all__'

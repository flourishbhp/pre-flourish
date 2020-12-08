from django import forms
from edc_form_validators import FormValidatorMixin

from ...models import PreFlourishDeathReport


class PreFlourishDeathReportForm(FormValidatorMixin, forms.ModelForm):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'subject_identifier')
        self.validate_against_consent_datetime(
            self.cleaned_data.get('report_datetime'))
        super().clean()

    class Meta:
        model = PreFlourishDeathReport
        fields = '__all__'

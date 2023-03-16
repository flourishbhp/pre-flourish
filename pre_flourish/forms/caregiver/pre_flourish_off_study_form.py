from django import forms
from edc_form_validators import FormValidatorMixin

from ...models import PreFlourishOffStudy


class PreFlourishOffStudyForm(FormValidatorMixin, forms.ModelForm):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get('subject_identifier')

        super().clean()

    class Meta:
        model = PreFlourishOffStudy
        fields = '__all__'

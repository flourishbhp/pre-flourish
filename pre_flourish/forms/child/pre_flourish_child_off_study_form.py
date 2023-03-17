from django import forms
from edc_form_validators import FormValidatorMixin

from ...models import PreFlourishChildOffStudy


class PreFlourishChildOffStudyForm(FormValidatorMixin, forms.ModelForm):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get('subject_identifier')
        super().clean()


    class Meta:
        model = PreFlourishChildOffStudy
        fields = '__all__'

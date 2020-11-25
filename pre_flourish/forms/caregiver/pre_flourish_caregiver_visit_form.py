from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ...models import PreFlourishCaregiverVisit


class PreFlourishCaregiverVisitForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    class Meta:
        model = PreFlourishCaregiverVisit
        fields = '__all__'

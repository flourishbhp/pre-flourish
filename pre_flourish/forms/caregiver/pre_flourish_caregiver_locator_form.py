from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ...models import PreFlourishCaregiverLocator


class PreFlourishCaregiverLocatorForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    class Meta:
        model = PreFlourishCaregiverLocator
        fields = '__all__'

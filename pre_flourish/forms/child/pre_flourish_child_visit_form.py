from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ...models import PreFlourishChildVisit


class PreFlourishChildVisitForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    class Meta:
        model = PreFlourishChildVisit
        fields = '__all__'

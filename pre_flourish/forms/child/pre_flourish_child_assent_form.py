from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from ...models import PreFlourishChildAssent


class PreFlourishChildAssentForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    class Meta:
        model = PreFlourishChildAssent
        fields = '__all__'
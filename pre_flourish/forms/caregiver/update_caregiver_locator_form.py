from django import forms

from ...models import UpdateCaregiverLocator


class UpdateCaregiverLocatorForm(forms.ModelForm):

    class Meta:
        model = UpdateCaregiverLocator
        fields = '__all__'

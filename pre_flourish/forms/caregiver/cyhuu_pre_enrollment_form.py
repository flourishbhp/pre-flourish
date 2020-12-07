from django import forms

from .form_mixins import SubjectModelFormMixin

from ...models import CyhuuPreEnrollment


class CyhuuPreEnrollmentForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = CyhuuPreEnrollment
        fields = '__all__'

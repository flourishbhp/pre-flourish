from django import forms

from .form_mixins import SubjectModelFormMixin
from ...form_validators import CyhuuPreEnrollmentFormValidator

from ...models import CyhuuPreEnrollment


class CyhuuPreEnrollmentForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = CyhuuPreEnrollmentFormValidator

    class Meta:
        model = CyhuuPreEnrollment
        fields = '__all__'

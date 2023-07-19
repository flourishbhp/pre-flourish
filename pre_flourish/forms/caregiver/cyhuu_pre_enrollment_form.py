from django import forms
from django.apps import apps as django_apps
from .form_mixins import SubjectModelFormMixin
from ...form_validators import CyhuuPreEnrollmentFormValidator

from ...models import CyhuuPreEnrollment


class CyhuuPreEnrollmentForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = CyhuuPreEnrollmentFormValidator
    screening_model = 'pre_flourish.preflourishsubjectscreening'
    consent_model = 'pre_flourish.preflourishconsent'

    @property
    def screening_model_cls(self):
        return django_apps.get_model(self.screening_model)

    @property
    def consent_model_cls(self):
        return django_apps.get_model(self.consent_model)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.subject_identifier = self.initial.get(
            'subject_identifier', None)

        self.initial['biological_mother'] = getattr(
            self.screening_obj, 'biological_mother')

    @property
    def screening_obj(self):
        try:
            return self.screening_model_cls.objects.get(
                screening_identifier=self.consent_obj_screening
            )
        except self.screening_model_cls.DoesNotExist:
            raise

    @property
    def consent_obj_screening(self):
        try:
            return self.consent_model_cls.objects.get(
                subject_identifier=self.subject_identifier
            ).screening_identifier

        except self.consent_model_cls.DoesNotExist:
            raise

    class Meta:
        model = CyhuuPreEnrollment
        fields = '__all__'

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
        self.pre_flourish_visit_obj = None

        pre_flourish_visit_id = self.initial.get('pre_flourish_visit', None)
        if pre_flourish_visit_id:
            try:
                self.pre_flourish_visit_obj = self.visit_model.objects.get(
                    id=pre_flourish_visit_id)
            except self.visit_model.DoesNotExist:
                self.pre_flourish_visit_obj = None

        if self.screening_obj:
            self.initial['biological_mother'] = getattr(
                self.screening_obj, 'biological_mother')

    @property
    def screening_obj(self):
        if self.consent_obj_screening:
            try:
                return self.screening_model_cls.objects.get(
                    screening_identifier=self.consent_obj_screening
                )
            except self.screening_model_cls.DoesNotExist:
                raise

    @property
    def consent_obj_screening(self):
        if self.pre_flourish_visit_obj:
            try:
                return self.consent_model_cls.objects.filter(
                    subject_identifier=self.pre_flourish_visit_obj.subject_identifier
                ).latest('consent_datetime').screening_identifier

            except self.consent_model_cls.DoesNotExist:
                raise

    class Meta:
        model = CyhuuPreEnrollment
        fields = '__all__'

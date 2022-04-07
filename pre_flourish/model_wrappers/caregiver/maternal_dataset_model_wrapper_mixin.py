from django.apps import apps as django_apps
from .maternal_screening_model_wrapper import PreFlourishMaternalScreeningModelWrapper


class MaternalDatasetModelWrapperMixin:
    subject_consent_model = 'pre_flourish.preflourishconsent'
    subject_screening_model = 'pre_flourish.preflourishsubjectscreening'
    subject_screening_wrapper_cls = PreFlourishMaternalScreeningModelWrapper

    @property
    def subject_consent_model_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    @property
    def subject_screening_model_cls(self):
        return django_apps.get_model(self.subject_screening_model)

    @property
    def subject_consent_obj(self):
        try:
            subject_consent = self.subject_consent_model_cls.objects.get(
                screening_identifier=self.object.screening_identifier)
        except self.subject_consent_model_cls.DoesNotExist:
            return None
        else:
            return subject_consent

    @property
    def subject_identifier(self):
        if self.subject_consent_obj:
            return self.subject_consent_obj.subject_identifier
        else:
            return ''

    @property
    def subject_screening_obj(self):
        try:
            subject_screening = self.subject_screening_model_cls.objects.get(
                screening_identifier=self.object.screening_identifier)
        except self.subject_screening_model_cls.DoesNotExist:
            return None
        else:
            return subject_screening

    @property
    def screening_identifier(self):
        if self.object:
            return self.object.screening_identifier
        else:
            return 'Not Set'

    @property
    def subject_screening_wrapper(self):

        model_object = self.subject_screening_obj or self.subject_screening_model_cls(
            **self.create_subject_screening_options
        )

        return self.subject_screening_wrapper_cls(model_obj=model_object)

    @property
    def create_subject_screening_options(self):
        options = dict(
            screening_identifier=self.object.screening_identifier
        )

        return options

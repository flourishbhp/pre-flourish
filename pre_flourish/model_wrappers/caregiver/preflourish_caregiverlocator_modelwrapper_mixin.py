
from django.apps import apps as django_apps

class PreflourishCaregiverLocatorModelWrapperMixin:
    @property
    def subject_consent_model_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    @property
    def subject_screening_model_cls(self):
        return django_apps.get_model(self.subject_screening_model)

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
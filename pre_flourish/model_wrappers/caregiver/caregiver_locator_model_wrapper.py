from edc_model_wrapper import ModelWrapper
from django.conf import settings
from django.apps import apps as django_apps
from .maternal_screening_model_wrapper import PreFlourishMaternalScreeningModelWrapper

class PreflourishCaregiverLocatorWrapper(ModelWrapper):
    model = 'flourish_caregiver.caregiverlocator'
    querystring_attrs = ['screening_identifier', 'subject_identifier',
                         'study_maternal_identifier', 'first_name', 'last_name']
    next_url_attrs = ['screening_identifier', 'subject_identifier',
                      'study_maternal_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'maternal_dataset_listboard_url')

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

        # breakpoint()

        model_object = self.subject_screening_obj or self.subject_screening_model_cls(
            **self.create_subject_screening_options
        )

        return self.subject_screening_wrapper_cls(model_obj=model_object)

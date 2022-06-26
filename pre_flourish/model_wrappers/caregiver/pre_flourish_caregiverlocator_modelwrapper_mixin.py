
from django.apps import apps as django_apps
from zmq import has
from .maternal_screening_model_wrapper import PreFlourishMaternalScreeningModelWrapper
from .log_entry_model_wrapper import PreFlourishLogEntryModelWrapper
from ...models import PreFlourishLogEntry

class PreflourishCaregiverLocatorModelWrapperMixin:

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
                previous_subject_identifier=self.previous_subject_identifier)
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

    @property
    def subject_consent_obj(self):
        if self.subject_screening_obj:
            try:
                subject_consent = self.subject_consent_model_cls.objects.get(
                    screening_identifier=self.subject_screening_obj.screening_identifier)                
            except self.subject_consent_model_cls.DoesNotExist:
                pass
            else:
                return subject_consent
              
    @property      
    def log_entry_model_wrapper(self):

        log_entry = PreFlourishLogEntry()
        if hasattr(self, 'subject_identifier'):
            # log_entry.subject_identifier = self.subject_identifier
            log_entry.study_maternal_identifier = self.subject_identifier
            
            
        return PreFlourishLogEntryModelWrapper(model_obj=log_entry)

    # def call_log_entry_objs(self):
    #     return
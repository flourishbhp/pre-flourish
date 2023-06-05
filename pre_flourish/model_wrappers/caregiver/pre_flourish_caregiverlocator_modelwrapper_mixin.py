from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .caregiver_locator_model_wrapper import PreflourishCaregiverLocatorModelWrapper
from .log_entry_model_wrapper import PreFlourishLogEntryModelWrapper
from ...models import PreFlourishLogEntry


class PreflourishCaregiverLocatorModelWrapperMixin:
    subject_consent_model = 'pre_flourish.preflourishconsent'
    subject_screening_model = 'pre_flourish.preflourishsubjectscreening'
    caregiver_locator_model_wrapper = PreflourishCaregiverLocatorModelWrapper

    @property
    def locator_model_obj(self):
        """Returns a caregiver locator model instance or None.
        """
        try:
            return self.caregiver_locator_cls.objects.get(
                **self.caregiver_locator_options)
        except ObjectDoesNotExist:
            return None

    @property
    def caregiver_locator(self):
        """"Returns a wrapped saved or unsaved caregiver locator
        """
        model_obj = self.locator_model_obj or self.caregiver_locator_cls(
            **self.create_caregiver_locator_options)
        return self.caregiver_locator_model_wrapper(model_obj=model_obj)

    @property
    def caregiver_locator_cls(self):
        return django_apps.get_model('flourish_caregiver.caregiverlocator')

    @property
    def create_caregiver_locator_options(self):
        """Returns a dictionary of options to create a new
        unpersisted caregiver locator model instance.
        """
        options = dict(
            screening_identifier=self.object.screening_identifier,
            subject_identifier=self.object.subject_identifier,
        )
        if (hasattr(self, 'study_maternal_identifier') and
                getattr(self, 'study_maternal_identifier')):
            options.update({'study_maternal_identifier': self.study_maternal_identifier})
        if hasattr(self, 'first_name'):
            options.update({'first_name': self.first_name, 'last_name': self.last_name})
        return options

    @property
    def caregiver_locator_options(self):
        """Returns a dictionary of options to get an existing
         caregiver locator model instance.
        """
        options = {}
        if getattr(self, 'study_maternal_identifier', None):
            options.update({'study_maternal_identifier': self.study_maternal_identifier})
        if (hasattr(self, 'screening_identifier') and
                getattr(self, 'screening_identifier')):
            options.update({'screening_identifier': self.object.screening_identifier})
        if (hasattr(self, 'subject_identifier') and
                getattr(self, 'subject_identifier')):
            options.update({'subject_identifier': self.object.subject_identifier})
        return options

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
                **self.create_subject_screening_options)
        except self.subject_screening_model_cls.DoesNotExist:
            return None
        else:
            return subject_screening

    @property
    def create_subject_screening_options(self):
        options = dict(
            study_maternal_identifier=self.object.study_maternal_identifier)
        if getattr(self, 'screening_identifier', None):
            options.update({'screening_identifier': self.object.screening_identifier})
        if getattr(self, 'subject_identifier', None):
            options.update({'subject_identifier': self.object.subject_identifier})

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

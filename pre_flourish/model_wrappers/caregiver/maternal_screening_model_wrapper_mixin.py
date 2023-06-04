from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist


class MaternalScreeningModelWrapperMixin:
    subject_screening_wrapper = None
    log_entry_model = 'pre_flourish_follow.preflourishlogentry'

    @property
    def screening_model_obj(self):
        """Returns a maternal model instance or None.
        """
        try:
            return self.maternal_screening_cls.objects.get(
                screening_identifier=self.object.screening_identifier)
        except ObjectDoesNotExist:
            return None

    @property
    def maternal_screening(self):
        """"Returns a wrapped saved or unsaved maternal screening
        """
        model_obj = self.screening_model_obj or self.maternal_screening_cls(
            **self.maternal_screening_options)
        return self.subject_screening_wrapper(model_obj=model_obj)

    @property
    def maternal_screening_cls(self):
        return django_apps.get_model('pre_flourish.preflourishsubjectscreening')

    @property
    def create_maternal_screening_options(self):
        """Returns a dictionary of options to create a new
        unpersisted maternal screening model instance.
        """
        options = dict(
            screening_identifier=self.object.screening_identifier)
        return options

    @property
    def log_entry_cls(self):
        return django_apps.get_model(self.log_entry_model)

    @property
    def maternal_screening_options(self):
        """Returns a dictionary of options to get an existing
        maternal screening model instance.
        """

        options = dict(
            screening_identifier=getattr(self.call_log_entry, 'screening_identifier', None),
            previous_subject_identifier=getattr(self.call_log_entry, 'study_maternal_identifier', None),
            willing_assent=getattr(self.call_log_entry, 'willing_assent', None),
            study_interest=getattr(self.call_log_entry, 'study_interest', None),
            willing_consent=getattr(self.call_log_entry, 'willing_consent', None),
            has_child=getattr(self.call_log_entry, 'has_child', None),
            caregiver_omang=getattr(self.call_log_entry, 'caregiver_omang', None),
        )
        return options

    @property
    def call_log_entry(self, **kwargs):
        """Returns a call log entry model instance.
        """

        call_log_entry = django_apps.get_model(self.log_entry_model).objects.filter(
            study_maternal_identifier=self.object.study_maternal_identifier).first()
        return call_log_entry

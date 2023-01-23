from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist


class MaternalScreeningModelWrapperMixin:
    subject_screening_wrapper = None

    @property
    def screening_model_obj(self):
        """Returns a maternal model instance or None.
        """
        try:
            return self.maternal_screening_cls.objects.get(
                **self.maternal_screening_options)
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
    def maternal_screening_options(self):
        """Returns a dictionary of options to get an existing
        maternal screening model instance.
        """
        options = dict(
            screening_identifier=self.object.screening_identifier)
        return options

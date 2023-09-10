from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from pre_flourish.model_wrappers.caregiver.caregiver_offstudy_model_wrapper import \
    CaregiverOffstudyModelWrapper


class CaregiverOffstudyModelWrapperMixin:
    caregiver_offstudy_model_wrapper_cls = CaregiverOffstudyModelWrapper

    @property
    def caregiver_offstudy_cls(self):
        return django_apps.get_model('pre_flourish.preflourishoffstudy')

    @property
    def caregiver_offstudy(self):
        """Returns a wrapped saved or unsaved caregiver death report.
        """
        model_obj = self.caregiver_offstudy_model_obj or \
                    self.caregiver_offstudy_cls(
                        **self.create_caregiver_offstudy_options)
        return CaregiverOffstudyModelWrapper(model_obj=model_obj)

    @property
    def create_caregiver_offstudy_options(self):
        """Returns a dictionary of options to create a new
        unpersisted caregiver death report model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier,
        )
        return options

    @property
    def caregiver_offstudy_options(self):
        """Returns a dictionary of options to get an existing
        caregiver death report model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def caregiver_offstudy_model_obj(self):
        """Returns a caregiver death report model instance or None.
        """
        try:
            return self.caregiver_offstudy_cls.objects.get(
                **self.caregiver_offstudy_options)
        except ObjectDoesNotExist:
            return None

    @property
    def show_dashboard(self):
        return True

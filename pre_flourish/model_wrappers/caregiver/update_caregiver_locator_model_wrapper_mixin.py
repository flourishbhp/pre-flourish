from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .update_caregiver_locator_model_wrapper import UpdateCaregiverLocatorModelWrapper


class UpdateCaregiverLocatorModelWrapperMixin:
    update_caregiver_locator_model_wrapper_cls = UpdateCaregiverLocatorModelWrapper

    @property
    def update_caregiver_locator_obj(self):
        """Returns a update caregiver locator model instance or None.
        """
        try:
            return self.update_caregiver_locator_cls.objects.get(
                **self.update_caregiver_locator_options)
        except ObjectDoesNotExist:
            return None

    @property
    def update_caregiver_locator(self):
        """"Returns a wrapped saved or unsaved update caregiver locator
        """
        model_obj = self.update_caregiver_locator_obj or \
                    self.update_caregiver_locator_cls(
                        **self.create_update_caregiver_locator_options)

        return self.update_caregiver_locator_model_wrapper_cls(model_obj=model_obj)

    @property
    def update_caregiver_locator_cls(self):
        return django_apps.get_model('pre_flourish.updatecaregiverlocator')

    @property
    def create_update_caregiver_locator_options(self):
        """Returns a dictionary of options to create a new
        unpersisted update caregiver locator model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier,
        )
        return options

    @property
    def update_caregiver_locator_options(self):
        """Returns a dictionary of options to get an existing
        update caregiver locator model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

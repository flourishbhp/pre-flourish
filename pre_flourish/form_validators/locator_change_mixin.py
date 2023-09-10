from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator


def raise_validation_error():
    message = 'Please update the caregiver locator before you continue'
    raise ValidationError(message)


class LocatorChangeMixin(FormValidator):
    locator_model = 'flourish_caregiver.caregiverlocator'

    @property
    def locator_cls(self):
        return django_apps.get_model(self.locator_model)

    def locator_obj_is_locator_updated(self, subject_identifier):

        try:
            obj = self.locator_cls.objects.get(
                subject_identifier=subject_identifier)
        except self.locator_cls.DoesNotExist:
            raise
        else:
            return obj.is_locator_updated

    def clean(self):
        self.validate_locator_updated()
        super().clean()

    def validate_locator_updated(self):
        cleaned_data = self.cleaned_data
        if self.locator_obj_is_locator_updated(cleaned_data.subject_identifier):
            raise_validation_error()

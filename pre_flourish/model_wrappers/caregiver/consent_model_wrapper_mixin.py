from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_consent.site_consents import site_consents

from flourish_dashboard.model_wrappers import SubjectConsentModelWrapper
from flourish_dashboard.model_wrappers.consent_model_wrapper_mixin import \
    ConsentModelWrapperMixin as BaseConsentModelWrapperMixin


class ConsentModelWrapperMixin(BaseConsentModelWrapperMixin):
    consent_model_wrapper_cls = SubjectConsentModelWrapper

    @property
    def screening_identifier(self):
        if self.object:
            return self.object.screening_identifier
        elif self.consent_older_version_model_obj:
            return self.consent_older_version_model_obj.screening_identifier
        return None

    @property
    def flourish_consent_object(self):
        """Returns a consent configuration object from site_consents
        relative to the wrapper's "object" report_datetime.
        """
        consent_model_wrapper_cls = self.consent_model_wrapper_cls or self.__class__

        default_consent_group = django_apps.get_app_config(
            'edc_consent').default_consent_group
        consent_object = site_consents.get_consent_for_period(
            model=consent_model_wrapper_cls.model,
            report_datetime=self.screening_report_datetime,
            consent_group=default_consent_group,
            version=self.consent_version or None)
        return consent_object

    @property
    def subject_consent_cls(self):
        return django_apps.get_model('flourish_caregiver.subjectconsent')

    @property
    def flourish_consent_model_obj(self):
        """Returns a consent model instance or None.
        """
        try:
            return self.subject_consent_cls.objects.get(**self.consent_options)
        except ObjectDoesNotExist:
            return None

    @property
    def flourish_consent(self):
        """Returns a wrapped saved or unsaved consent.
        """
        model_obj = self.flourish_consent_model_obj or self.subject_consent_cls(
            **self.create_consent_options)
        return self.consent_model_wrapper_cls(model_obj=model_obj)

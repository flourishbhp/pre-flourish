from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_base.utils import get_uuid
from flourish_dashboard.model_wrappers.child_dummy_consent_model_wrapper_mixin import \
    ChildDummyConsentModelWrapperMixin


class ChildConsentModelWrapperMixin(ChildDummyConsentModelWrapperMixin):
    consent_model_wrapper_cls = None

    @property
    def subject_consent_cls(self):
        return django_apps.get_model('pre_flourish.preflourishconsent')

    @property
    def child_consent(self):
        """
        Returns a consent objects of the child from the caregiver consent
        """
        return self.subject_consent_cls.objects.filter(
            subject_identifier=self.object.subject_identifier).latest('consent_datetime')

    @property
    def consent_model_obj(self):
        """Returns a consent model instance or None.
        """
        try:
            return self.subject_consent_cls.objects.get(**self.consent_options)
        except ObjectDoesNotExist:
            return None
    @property
    def consent(self):
        """Returns a wrapped saved or unsaved consent.
        """
        model_obj = self.consent_model_obj or self.subject_consent_cls(
            **self.create_consent_options)
        return self.consent_model_wrapper_cls(model_obj=model_obj)

    @property
    def create_consent_options(self):
        """Returns a dictionary of options to create a new
        unpersisted consent model instance.
        """
        return dict(
            screening_identifier=self.screening_identifier,
            consent_identifier=get_uuid(),
        )

    @property
    def consent_options(self):
        """Returns a dictionary of options to get an existing
        consent model instance.
        """
        options = dict(
            screening_identifier=self.object.screening_identifier,
            version=self.consent_version)
        return options

    @property
    def child_consents(self):
        if self.consent_model_obj:
            return self.consent_model_obj.caregiverchildconsent_set.all()
        return []

    @property
    def get_cohort(self):
        pass

    @property
    def maternal_delivery_obj(self):
        pass

    @property
    def get_assent(self):
        pass

    @property
    def get_antenatal(self):
        pass

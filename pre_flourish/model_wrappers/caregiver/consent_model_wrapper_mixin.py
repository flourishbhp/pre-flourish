from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_base.utils import get_uuid

from edc_consent.site_consents import site_consents

pre_flourish_config = django_apps.get_app_config('pre_flourish')


class ConsentModelWrapperMixin:
    consent_model_wrapper_cls = None

    @property
    def screening_identifier(self):
        if self.object:
            return self.object.screening_identifier
        elif self.consent_older_version_model_obj:
            return self.consent_older_version_model_obj.screening_identifier
        return None

    @property
    def consent_object(self):
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
        return django_apps.get_model('pre_flourish.preflourishconsent')

    @property
    def consent_version_cls(self):
        return django_apps.get_model('pre_flourish.pfconsentversion')

    def get_consent_version(self, default_version):
        try:
            consent_version_obj = self.consent_version_cls.objects.get(
                screening_identifier=self.screening_identifier)
        except self.consent_version_cls.DoesNotExist:
            return default_version
        else:
            return consent_version_obj.version

    @property
    def consent_version(self):
        return self.get_consent_version(pre_flourish_config.consent_version)

    @property
    def child_consent_version(self):
        return self.get_consent_version(pre_flourish_config.child_consent_version)

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
        options = dict(
            screening_identifier=self.screening_identifier,
            consent_identifier=get_uuid(),
            version=self.consent_version
        )
        return options

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
            return self.consent_model_obj.preflourishcaregiverchildconsent_set.all()
        return []

    @property
    def children_eligibility(self):
        if self.object.preflourishcaregiverchildconsent_set.all():
            eligible_children = self.object.preflourishcaregiverchildconsent_set.filter(
                is_eligible=True)
            return False if not eligible_children else True
        return True

    @property
    def children_ineligible(self):
        if self.child_consents:
            return self.child_consents.filter(is_eligible=False)
        return []

    @property
    def consent_older_version_model_obj(self):
        """Returns a consent version 1 model instance or None.
        """
        consents = self.subject_consent_cls.objects.filter(
            screening_identifier=self.object.screening_identifier)
        if consents:
            return consents.latest('consent_datetime')

from django.apps import apps as django_apps
from django.conf import settings
from edc_base.utils import get_uuid
from edc_model_wrapper import ModelWrapper

from .consent_model_wrapper_mixin import ConsentModelWrapperMixin
from .pre_flourish_caregiverlocator_modelwrapper_mixin import \
    PreflourishCaregiverLocatorModelWrapperMixin
from .pre_flourish_subject_consent_model_wrapper import \
    PreFlourishSubjectConsentModelWrapper
from ..pf_consent_version_model_wrapper_mixin import PfConsentVersionModelWrapperMixin


class PreFlourishMaternalScreeningModelWrapper(PfConsentVersionModelWrapperMixin,
                                               PreflourishCaregiverLocatorModelWrapperMixin,
                                               ConsentModelWrapperMixin,
                                               ModelWrapper):
    consent_model_wrapper_cls = PreFlourishSubjectConsentModelWrapper
    model = 'pre_flourish.preflourishsubjectscreening'
    querystring_attrs = ['screening_identifier',
                         'study_maternal_identifier',
                         'willing_assent',
                         'study_interest',
                         'willing_consent',
                         'has_child',
                         'caregiver_omang'
                         ]

    next_url_attrs = ['screening_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'pre_flourish_screening_listboard_url')

    @property
    def subject_identifier(self):
        if self.consent_older_version_model_obj:
            return self.consent_older_version_model_obj.subject_identifier
        return None

    @property
    def subject_consent_cls(self):
        return django_apps.get_model('pre_flourish.preflourishconsent')

    @property
    def create_consent_options(self):
        """Returns a dictionary of options to create a new
        unpersisted consent model instance.
        """
        options = dict(
            screening_identifier=self.screening_identifier,
            consent_identifier=get_uuid(),
            version=self.consent_version)
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

    def is_eligible(self):
        return self.object.is_eligible

    def eligible_at_enrol(self):
        return self.object.is_eligible

    @property
    def screening_report_datetime(self):
        return self.object.report_datetime

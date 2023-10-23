from django.apps import apps as django_apps
from django.conf import settings
from django.db.models import Q
from edc_constants.constants import YES
from edc_model_wrapper import ModelWrapper

from .log_entry_model_wrapper import PreFlourishLogEntryModelWrapper
from .maternal_screening_model_wrapper_mixin import MaternalScreeningModelWrapperMixin


class PreflourishCaregiverLocatorModelWrapper(MaternalScreeningModelWrapperMixin,
                                              ModelWrapper):
    subject_screening_wrapper = None
    model = 'flourish_caregiver.caregiverlocator'
    querystring_attrs = ['screening_identifier', 'subject_identifier',
                         'study_maternal_identifier', 'first_name', 'last_name']
    inperson_contact_model = 'pre_flourish_follow.preflourishinpersoncontactattempt'
    log_entry_model = 'pre_flourish_follow.preflourishlogentry'

    @property
    def next_url_name(self):
        url_name = None
        if not self.object.subject_identifier:
            url_name = settings.DASHBOARD_URL_NAMES.get(
                'pre_flourish_caregiver_locator_listboard_url')
        else:
            url_name = settings.DASHBOARD_URL_NAMES.get(
                'pre_flourish_subject_dashboard_url')
        return url_name

    @property
    def next_url_attrs(self):
        next_url_attrs = []
        if not self.object.subject_identifier:
            next_url_attrs = ['study_maternal_identifier']
        else:
            next_url_attrs = ['subject_identifier']
        return next_url_attrs

    @property
    def inperson_contact_cls(self):
        return django_apps.get_model(self.inperson_contact_model)

    @property
    def log_entry_cls(self):
        return django_apps.get_model(self.log_entry_model)

    @property
    def study_maternal_identifier(self):
        return self.object.study_maternal_identifier

    @property
    def call_or_home_visit_success(self):
        """Returns true if the call or home visit was a success.
        """
        log_entries = self.log_entry_cls.objects.filter(
            ~Q(phone_num_success='none_of_the_above'),
            study_maternal_identifier=self.object.study_maternal_identifier,
            phone_num_success__isnull=False)
        home_visit_logs = self.inperson_contact_cls.objects.filter(
            ~Q(successful_location='none_of_the_above'),
            study_maternal_identifier=self.object.study_maternal_identifier,
            successful_location__isnull=False)
        if log_entries:
            return True
        elif home_visit_logs:
            return True
        return False

    @property
    def call_log_model_objs(self):
        log_entries = self.log_entry_cls.objects.filter(
            study_maternal_identifier=self.object.study_maternal_identifier
        )

        return log_entries

    @property
    def eligible_status(self):
        try:
            log_entry = self.call_log_model_objs.latest('call_datetime')
        except self.log_entry_cls.DoesNotExist:
            return False
        else:
            return log_entry.has_child == YES

    @property
    def call_log_model_wrappers(self):

        log_entry_wrappers = []

        for entry in self.call_log_model_objs:
            log_entry_wrappers.append(
                PreFlourishLogEntryModelWrapper(model_obj=entry)
            )

        return log_entry_wrappers

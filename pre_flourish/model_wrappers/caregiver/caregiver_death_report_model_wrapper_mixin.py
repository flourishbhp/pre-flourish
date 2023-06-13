from django.apps import apps as django_apps
from flourish_dashboard.model_wrappers.caregiver_death_report_model_wrapper_mixin import \
    CaregiverDeathReportModelWrapperMixin as BaseCaregiverDeathReportModelWrapperMixin
from .caregiver_death_report_model_wrapper import CaregiverDeathReportModelWrapper


class CaregiverDeathReportModelWrapperMixin(BaseCaregiverDeathReportModelWrapperMixin):
    caregiver_death_report_model_wrapper_cls = CaregiverDeathReportModelWrapper

    @property
    def caregiver_death_report(self):
        """"Returns a wrapped saved or unsaved caregiver death report
        """
        model_obj = self.caregiver_death_report_obj or self.caregiver_death_report_cls(
            **self.create_caregiver_death_report_options)

        return CaregiverDeathReportModelWrapper(model_obj=model_obj)

    @property
    def caregiver_death_report_cls(self):
        return django_apps.get_model('pre_flourish.preflourishdeathreport')

    @property
    def create_caregiver_death_report_options(self):
        """Returns a dictionary of options to create a new
        unpersisted caregiver death report model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier,
        )
        return options

    @property
    def caregiver_death_report_options(self):
        """Returns a dictionary of options to get an existing
        caregiver death report model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

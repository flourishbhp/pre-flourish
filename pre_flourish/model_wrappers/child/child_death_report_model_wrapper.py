from django.conf import settings

from flourish_dashboard.model_wrappers.child_death_report_model_wrapper import \
    ChildDeathReportModelWrapper as BaseChildDeathReportModelWrapper


class ChildDeathReportModelWrapper(BaseChildDeathReportModelWrapper):
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'pre_flourish_child_dashboard_url')

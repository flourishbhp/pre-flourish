from django.conf import settings
from edc_model_wrapper import ModelWrapper


class CaregiverDeathReportModelWrapper(ModelWrapper):
    model = 'pre_flourish.preflourishdeathreport'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'pre_flourish_subject_dashboard_url')
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['subject_identifier']

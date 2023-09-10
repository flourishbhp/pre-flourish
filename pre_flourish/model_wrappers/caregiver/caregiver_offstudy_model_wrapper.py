from django.conf import settings
from edc_model_wrapper import ModelWrapper


class CaregiverOffstudyModelWrapper(ModelWrapper):
    model = 'pre_flourish.preflourishoffstudy'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'pre_flourish_subject_dashboard_url')
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['subject_identifier']

from django.conf import settings
from edc_model_wrapper import ModelWrapper


class PreFlourishDataActionItemModelWrapper(ModelWrapper):

    model = 'edc_data_manager.dataactionitem'
    next_url_attrs = ['subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'pre_flourish_subject_dashboard_url')

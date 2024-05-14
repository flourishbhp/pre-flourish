from django.conf import settings
from edc_model_wrapper import ModelWrapper


class PreFlourishContactModelWrapper(ModelWrapper):

    model = 'pre_flourish.preflourishcontact'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'pre_flourish_child_dashboard_url')
    next_url_attrs = ['subject_identifier', ]
    querystring_attrs = ['subject_identifier', ]

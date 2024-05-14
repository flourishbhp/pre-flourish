from django.conf import settings
from edc_model_wrapper import ModelWrapper


class PreFlourishChildAssentModelWrapper(ModelWrapper):
    model = 'pre_flourish.preflourishchildassent'
    next_url_name = settings.DASHBOARD_URL_NAMES.get('pre_flourish_subject_dashboard_url')
    querystring_attrs = ['subject_identifier', 'dob',
                         'first_name', 'last_name', 'initials', 'gender',
                         'identity', 'identity_type', 'confirm_identity',
                         'dob']
    next_url_attrs = ['screening_identifier', 'subject_identifier']

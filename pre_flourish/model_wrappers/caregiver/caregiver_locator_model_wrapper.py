from django.conf import settings
from edc_model_wrapper import ModelWrapper


class PreflourishCaregiverLocatorModelWrapper(ModelWrapper):
    model = 'flourish_caregiver.caregiverlocator'
    querystring_attrs = ['screening_identifier', 'subject_identifier',
                         'study_maternal_identifier', 'first_name', 'last_name']
    next_url_attrs = ['screening_identifier', 'subject_identifier',
                      'study_maternal_identifier', ]
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'pre_flourish_screening_listboard_url')

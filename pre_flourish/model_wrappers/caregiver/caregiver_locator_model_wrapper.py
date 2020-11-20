from django.conf import settings

from edc_model_wrapper import ModelWrapper


class CaregiverLocatorModelWrapper(ModelWrapper):

    model = 'pre_flourish.caregiverlocator'
    querystring_attrs = ['screening_identifier', 'subject_identifier',
                         'study_maternal_identifier']
    next_url_attrs = ['screening_identifier', 'subject_identifier',
                      'study_maternal_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')

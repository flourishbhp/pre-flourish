from django.conf import settings

from edc_model_wrapper import ModelWrapper


class PreFlourishCaregiverLocatorModelWrapper(ModelWrapper):

    model = 'pre_flourish.preflourishcaregiverlocator'
    querystring_attrs = ['screening_identifier', 'subject_identifier',
                         'study_maternal_identifier']
    next_url_attrs = ['screening_identifier', 'subject_identifier',
                      'study_maternal_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'pre_flourish_subject_dashboard_url')

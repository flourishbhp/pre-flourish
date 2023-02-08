from django.conf import settings
from edc_model_wrapper import ModelWrapper

from pre_flourish.model_wrappers.child.child_assent_model_wrapper_mixin import \
    ChildAssentModelWrapperMixin


class CaregiverChildConsentModelWrapper(ChildAssentModelWrapperMixin,ModelWrapper):
    model = 'pre_flourish.preflourishcaregiverchildconsent'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'pre_flourish_child_dashboard_url')
    next_url_attrs = ['subject_identifier', 'screening_identifier']
    querystring_attrs = ['subject_identifier', 'screening_identifier']

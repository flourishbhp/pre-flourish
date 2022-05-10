from edc_model_wrapper import ModelWrapper
from django.conf import settings
from django.apps import apps as django_apps
from .maternal_screening_model_wrapper import PreFlourishMaternalScreeningModelWrapper
from .preflourish_caregiverlocator_modelwrapper_mixin import PreflourishCaregiverLocatorModelWrapperMixin

class PreflourishCaregiverLocatorModelWrapper(ModelWrapper, PreflourishCaregiverLocatorModelWrapperMixin):
    model = 'flourish_caregiver.caregiverlocator'
    querystring_attrs = ['screening_identifier', 'subject_identifier',
                         'study_maternal_identifier', 'first_name', 'last_name']
    next_url_attrs = ['screening_identifier', 'subject_identifier',
                      'study_maternal_identifier',]
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'maternal_dataset_listboard_url')

    @property
    def previous_subject_identifier(self):
        return self.object.study_maternal_identifier

    

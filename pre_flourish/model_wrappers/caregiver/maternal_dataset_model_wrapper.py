from django.apps import apps as django_apps
from django.conf import settings
from django.db.models import Q
from edc_model_wrapper import ModelWrapper
from .maternal_dataset_model_wrapper_mixin import MaternalDatasetModelWrapperMixin


class MaternalDatasetModelWrapper(MaternalDatasetModelWrapperMixin,
                                  ModelWrapper):
    model = 'flourish_caregiver.maternaldataset'
    querystring_attrs = [
        'screening_identifier', 'subject_identifier',
        'study_maternal_identifier', 'study_child_identifier']
    next_url_attrs = ['study_maternal_identifier', 'screening_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'maternal_dataset_listboard_url')

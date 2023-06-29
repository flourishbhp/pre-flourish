from django.conf import settings
from edc_model_wrapper import ModelWrapper

from flourish_dashboard.model_wrappers.bhp_prior_screening_model_wrapper import \
    BHPPriorScreeningModelWrapper as BaseScreeningModelWrapper


class BHPPriorScreeningModelWrapper(BaseScreeningModelWrapper):

    next_url_attrs = ['study_maternal_identifier']

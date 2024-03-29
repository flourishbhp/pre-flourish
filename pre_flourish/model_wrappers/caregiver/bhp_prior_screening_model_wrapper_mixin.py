from flourish_dashboard.model_wrappers.bhp_prior_screening_model_wrapper_mixin import \
    BHPPriorScreeningModelWrapperMixin as BaseScreeningModelWrapperMixin
from pre_flourish.model_wrappers.caregiver.bhp_prior_screening_model_wrapper import \
    BHPPriorScreeningModelWrapper


class BhpPriorScreeningModelWrapperMixin(BaseScreeningModelWrapperMixin):
    prior_screening_model_wrapper_cls = BHPPriorScreeningModelWrapper

    @property
    def create_bhp_prior_screening_options(self):
        """Returns a dictionary of options to create a new
        unpersisted bhp prior screening model instance.
        """
        options = dict(
            screening_identifier=self.screening_identifier,
            study_maternal_identifier=self.locator_model_obj.study_maternal_identifier,
        )
        return options

    @property
    def bhp_prior_screening_options(self):
        """Returns a dictionary of options to get an existing
        maternal screening model instance.
        """
        options = dict(
            screening_identifier=self.screening_identifier, )
        return options

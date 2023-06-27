from flourish_caregiver.models import CaregiverLocator, MaternalDataset
from flourish_child.models import ChildDataset
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
            screening_identifier=getattr(self, 'get_or_create_dataset',
                                         'locator_model_obj').screening_identifier,
            study_maternal_identifier=getattr(self, 'get_or_create_dataset',
                                              'locator_model_obj').study_maternal_identifier,
        )
        return options

    @property
    def bhp_prior_screening_options(self):
        """Returns a dictionary of options to get an existing
        maternal screening model instance.
        """
        options = dict(
            screening_identifier=getattr(self, 'get_or_create_dataset',
                                         'locator_model_obj').screening_identifier, )
        return options

    @property
    def get_or_create_dataset(self):
        defaults = {
            'first_name': self.locator_model_obj.first_name,
            'last_name': self.locator_model_obj.last_name,
            'protocol': 'BCPP',
            'screening_identifier': self.locator_model_obj.screening_identifier
        }
        obj, _ = MaternalDataset.objects.get_or_create(
            defaults=defaults,
            study_maternal_identifier=self.locator_model_obj.study_maternal_identifier, )
        return obj

    def create_child_dataset(self):
        defaults = {
            'first_name': '',
            'last_name': '',
            'protocol': '',
            'dob': '',
            'age_today': '',
            'infant_sex': '',
            'infant_hiv_exposed': '',
            'infant_hiv_status': '',
            'infant_breastfed': '',
            'infant_breastfed_days': '',
            'weaned': '',
            'weandt': '',
        }
        ChildDataset.objects.get_or_create(
            defaults=defaults,
            study_maternal_identifier=self.locator_model_obj.study_maternal_identifier, )

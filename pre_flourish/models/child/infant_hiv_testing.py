from flourish_child.models.model_mixins.hiv_testing_model_mixin import \
    HivTestingModelMixin
from pre_flourish.models.model_mixins import CrfModelMixin


class PFInfantHIVTesting(CrfModelMixin, HivTestingModelMixin):
    class Meta(CrfModelMixin.Meta):
        app_label = 'pre_flourish'
        verbose_name = 'Infant HIV Testing and Results CRF'
        verbose_name_plural = 'Infant HIV Testing and Results CRFs'

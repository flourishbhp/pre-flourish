from flourish_child.models.model_mixins.hiv_rapid_test_conseling_model_mixin import \
    HivRapidTestCounselingModelMixin
from pre_flourish.models.model_mixins import CrfModelMixin


class PFChildHIVRapidTestCounseling(HivRapidTestCounselingModelMixin, CrfModelMixin):
    class Meta(CrfModelMixin.Meta):
        app_label = 'pre_flourish'
        verbose_name = 'Child HIV Rapid Testing and Counseling'
        verbose_name_plural = 'Child HIV Rapid Testing and Counseling'

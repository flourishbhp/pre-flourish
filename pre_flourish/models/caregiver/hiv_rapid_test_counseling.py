from flourish_child.models.model_mixins.hiv_rapid_test_conseling_model_mixin import \
    HivRapidTestCounselingModelMixin
from pre_flourish.models.model_mixins import CrfModelMixin


class PFHIVRapidTestCounseling(HivRapidTestCounselingModelMixin, CrfModelMixin):
    class Meta(CrfModelMixin.Meta):
        app_label = 'pre_flourish'
        verbose_name = 'HIV Rapid Testing and Counseling'
        verbose_name_plural = 'HIV Rapid Testing and Counseling'

from flourish_child.models.model_mixins.preg_test_model_mixin import PregTestModelMixin
from ..model_mixins import CrfModelMixin


class PFChildPregTesting(CrfModelMixin, PregTestModelMixin):
    class Meta(CrfModelMixin.Meta):
        app_label = 'pre_flourish'
        verbose_name = 'Pregnancy Testing for Female Adolescents'
        verbose_name_plural = 'Pregnancy Testing for Female Adolescents'

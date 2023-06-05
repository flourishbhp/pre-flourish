from django.db import models
from edc_constants.choices import YES_NO

from ..model_mixins import CrfModelMixin


class UpdateCaregiverLocator(CrfModelMixin):
    is_locator_updated = models.CharField(
        verbose_name='Did you update caregiver locator information',
        choices=YES_NO,
        null=True,
        max_length=5
    )

    class Meta(CrfModelMixin.Meta):
        app_label = 'pre_flourish'
        verbose_name = 'Update Caregiver Locator'
        verbose_name_plural = 'Update Caregiver Locators'

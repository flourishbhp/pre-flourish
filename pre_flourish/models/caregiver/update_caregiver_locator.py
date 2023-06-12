from django.db import models
from edc_base import get_utcnow
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_constants.choices import YES_NO
from edc_protocol.validators import datetime_not_before_study_start


class UpdateCaregiverLocator(BaseUuidModel):
    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        null=True)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        default=get_utcnow,
        help_text=('If reporting today, use today\'s date/time, otherwise use '
                   'the date/time this information was reported.'))

    is_locator_updated = models.CharField(
        verbose_name='Did you update caregiver locator information',
        choices=YES_NO,
        null=True,
        max_length=5
    )

    class Meta:
        app_label = 'pre_flourish'
        verbose_name = 'Update Caregiver Locator'
        verbose_name_plural = 'Update Caregiver Locators'

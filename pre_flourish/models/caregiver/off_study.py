from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators.date import datetime_not_future
from edc_base.utils import get_utcnow
from edc_identifier.managers import SubjectIdentifierManager
from edc_protocol.validators import datetime_not_before_study_start

from edc_action_item.model_mixins import ActionModelMixin
from edc_visit_schedule.model_mixins import OffScheduleModelMixin
from edc_visit_schedule.site_visit_schedules import site_visit_schedules



class OffStudy(OffScheduleModelMixin,
                       ActionModelMixin, BaseUuidModel):

    tracking_identifier_prefix = 'MO'
    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        default=get_utcnow,
        help_text=('If reporting today, use today\'s date/time, otherwise use'
                   ' the date/time this information was reported.'))

    reason = models.CharField(
        verbose_name=('Please code the primary reason participant taken'
                      ' off-study'),
        max_length=115)

    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    def take_off_schedule(self):
        pass
    
    
    class Meta:
        app_label = 'pre_flourish'
        verbose_name = 'Off Study'
        verbose_name_plural = 'Off Studies'

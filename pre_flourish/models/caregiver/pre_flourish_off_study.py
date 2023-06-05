from django.apps import apps as django_apps
from edc_visit_schedule import site_visit_schedules
from django.db import models
from pre_flourish.action_items import MATERNAL_OFF_STUDY_ACTION
from pre_flourish.models.caregiver.model_mixins.off_study_mixin import OffStudyMixin
from pre_flourish.choices import CAREGIVER_OFF_STUDY_REASON


class PreFlourishOffStudy(OffStudyMixin):
    action_name = MATERNAL_OFF_STUDY_ACTION
    reason = models.CharField(
        verbose_name='Please code the primary reason participant taken'
                     ' off-study',
        choices=CAREGIVER_OFF_STUDY_REASON,
        max_length=300,
    )

    class Meta:
        app_label = 'pre_flourish'
        verbose_name = 'Maternal Off Study'
        verbose_name_plural = 'Maternal Off Studies'

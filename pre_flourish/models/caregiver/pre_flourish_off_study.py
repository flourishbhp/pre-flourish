from django.apps import apps as django_apps
from edc_visit_schedule import site_visit_schedules

from pre_flourish.action_items import MATERNAL_OFF_STUDY_ACTION
from pre_flourish.models.caregiver.model_mixins.off_study_mixin import OffStudyMixin


class PreFlourishOffStudy(OffStudyMixin):
    action_name = MATERNAL_OFF_STUDY_ACTION

    class Meta:
        app_label = 'pre_flourish'
        verbose_name = 'Maternal Off Study'
        verbose_name_plural = 'Maternal Off Studies'

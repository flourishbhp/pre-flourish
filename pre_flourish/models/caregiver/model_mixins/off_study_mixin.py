from django.apps import apps as django_apps
from django.db import models
from django.forms import forms
from edc_action_item.model_mixins import ActionModelMixin
from edc_base import get_utcnow
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future, date_not_future
from edc_identifier.managers import SubjectIdentifierManager
from edc_protocol.validators import datetime_not_before_study_start, \
    date_not_before_study_start
from edc_visit_schedule import site_visit_schedules
from edc_visit_schedule.model_mixins import OffScheduleModelMixin

from flourish_prn.action_items import CAREGIVEROFF_STUDY_ACTION
from flourish_prn.models.offstudy_model_mixin import OffStudyModelMixin
from pre_flourish.models.caregiver.pre_flourish_consent import PreFlourishConsent


class OffStudyMixin(OffStudyModelMixin, OffScheduleModelMixin,
                    ActionModelMixin, BaseUuidModel):
    tracking_identifier_prefix = 'MO'

    action_name = CAREGIVEROFF_STUDY_ACTION
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

    offstudy_date = models.DateField(
        verbose_name="Off-study Date",
        validators=[
            date_not_before_study_start,
            date_not_future])

    reason_other = OtherCharField()

    comment = models.TextField(
        max_length=250,
        verbose_name="Comment",
        blank=True,
        null=True)

    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    def take_off_schedule(self):
        history_model = 'edc_visit_schedule.subjectschedulehistory'
        history_cls = django_apps.get_model(history_model)
        onschedules = history_cls.objects.onschedules(
            subject_identifier=self.subject_identifier,
            report_datetime=self.report_datetime)

        if onschedules:
            for onschedule in onschedules:
                _, schedule = \
                    site_visit_schedules.get_by_onschedule_model_schedule_name(
                        onschedule_model=onschedule._meta.label_lower,
                        name=onschedule.schedule_name)

                schedule.take_off_schedule(
                    subject_identifier=self.subject_identifier,
                    offschedule_datetime=self.report_datetime,
                    schedule_name=onschedule.schedule_name)

    def get_consent_version(self):
        try:
            consent_obj = PreFlourishConsent.objects.get(
                subject_identifier=self.subject_identifier)
        except PreFlourishConsent.DoesNotExist:
            raise forms.ValidationError(
                'Missing Consent Version form. Please complete '
                'it before proceeding.')
        else:
            return consent_obj.version


    class Meta:
        abstract = True

from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_mixins import BaseUuidModel, FormAsJSONModelMixin
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_consent.model_mixins import RequiresConsentFieldsModelMixin
from edc_metadata.model_mixins.updates import UpdatesCrfMetadataModelMixin
from edc_reference.model_mixins import ReferenceModelMixin
from edc_visit_schedule.model_mixins import SubjectScheduleCrfModelMixin
from edc_visit_tracking.model_mixins import CrfModelMixin as BaseCrfModelMixin
from edc_visit_tracking.model_mixins import PreviousVisitModelMixin

from ..pre_flourish_visit import PreFlourishVisit

pre_flourish_config = django_apps.get_app_config('pre_flourish')


class CrfModelMixin(BaseCrfModelMixin, SubjectScheduleCrfModelMixin,
                    RequiresConsentFieldsModelMixin, PreviousVisitModelMixin,
                    UpdatesCrfMetadataModelMixin, SiteModelMixin,
                    FormAsJSONModelMixin, ReferenceModelMixin, BaseUuidModel):
    """ Base model for all scheduled models
    """
    offschedule_compare_dates_as_datetimes = True
    pre_flourish_visit = models.OneToOneField(PreFlourishVisit, on_delete=PROTECT)
    crf_date_validator_cls = None

    @property
    def subject_identifier(self):
        return self.pre_flourish_visit.appointment.subject_identifier

    def natural_key(self):
        return self.pre_flourish_visit.natural_key()

    def get_consent_version(self):
        pf_subject_screening_cls = django_apps.get_model(
            'pre_flourish.preflourishsubjectscreening')

        consent_version_cls = django_apps.get_model(
            'pre_flourish.pfconsentversion')

        subject_identifier = self.subject_identifier

        if len(self.subject_identifier.split('-')) == 4:
            subject_identifier = self.subject_identifier[:-3]

        try:
            subject_screening_obj = pf_subject_screening_cls.objects.get(
                subject_identifier=subject_identifier)
        except pf_subject_screening_cls.DoesNotExist:
            raise ValidationError(
                'Missing Subject Screening form. Please complete '
                'it before proceeding.')
        else:
            screening_identifier = getattr(
                subject_screening_obj, 'screening_identifier', None)

            try:
                consent_version_obj = consent_version_cls.objects.get(
                    screening_identifier=screening_identifier)
            except consent_version_cls.DoesNotExist:
                raise ValidationError(
                    'Missing Consent Version form. Please complete '
                    'it before proceeding.')
            else:
                return consent_version_obj.version

    def save(self, *args, **kwargs):
        self.consent_version = self.get_consent_version()
        super().save(*args, **kwargs)

    natural_key.dependencies = ['pre_flourish.pre_flourish_visit']

    class Meta:
        abstract = True

from statistics import mode
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.sites import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_protocol.validators import datetime_not_before_study_start
from edc_search.model_mixins import SearchSlugManager

from pre_flourish_follow.models import EligibilityMixin
from ...identifiers import ScreeningIdentifier
from .eligibility import Eligibility
from .model_mixins import SearchSlugModelMixin
from flourish_caregiver.models.caregiver_locator import CaregiverLocator


class PreFlourishSubjectScreeningManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, eligibility_identifier):
        return self.get(screening_identifier=eligibility_identifier)


class PreFlourishSubjectScreening(EligibilityMixin,NonUniqueSubjectIdentifierFieldMixin,
                                  SiteModelMixin, SearchSlugModelMixin, BaseUuidModel):
    """ A model completed by the user to test and capture the result of
    the pre-consent eligibility checks.

    This model has no PII.
    """
    identifier_cls = ScreeningIdentifier

    screening_identifier = models.CharField(
        verbose_name="Eligibility Identifier",
        max_length=36,
        blank=True,
        null=True,
        unique=True)

    study_maternal_identifier = models.CharField(
        verbose_name='Study Maternal Identifier',
        max_length=17,
        null=True, )

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        default=get_utcnow,
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        help_text='Date and time of assessing eligibility')

    caregiver_age = models.IntegerField(
        verbose_name='What is the age of the caregiver?')

    remain_in_study = models.CharField(
        max_length=3,
        verbose_name='Are you willing to remain in the study area until 2025?',
        choices=YES_NO,
        help_text='If no, participant is not eligible.')

    ineligibility = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
        editable=False)

    is_eligible = models.BooleanField(
        default=False,
        editable=False)
    # is updated via signal once subject is consented
    is_consented = models.BooleanField(
        default=False,
        editable=False)
    # updated by signal on saving consent, is determined by participant
    # citizenship
    has_passed_consent = models.BooleanField(
        default=False,
        editable=False)

    history = HistoricalRecords()

    class Meta:
        app_label = 'pre_flourish'
        verbose_name = "Caregiver Eligibility"
        verbose_name_plural = "Caregiver Eligibility"

    def save(self, *args, **kwargs):
        eligibility_criteria = Eligibility(self.willing_consent,
                                           self.has_child,
                                           self.caregiver_age,
                                           self.caregiver_omang,
                                           self.willing_assent,
                                           self.study_interest,
                                           self.remain_in_study)

        self.is_eligible = eligibility_criteria.is_eligible
        self.ineligibility = eligibility_criteria.error_message

        if not self.screening_identifier:
            self.screening_identifier = self.identifier_cls().identifier

        super(PreFlourishSubjectScreening, self).save(*args, **kwargs)

    def natural_key(self):
        return self.screening_identifier

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('screening_identifier')
        return fields

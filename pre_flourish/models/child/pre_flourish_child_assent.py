from django.apps import apps as django_apps
from django.db import models
from django_crypto_fields.fields import IdentityField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_consent.field_mixins import CitizenFieldsMixin, ReviewFieldsMixin, \
    VerificationFieldsMixin, VulnerabilityFieldsMixin
from edc_consent.field_mixins import IdentityFieldsMixin, PersonalFieldsMixin
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_protocol.validators import datetime_not_before_study_start
from edc_search.model_mixins import SearchSlugManager

from flourish_caregiver.choices import CHILD_IDENTITY_TYPE


class PreFlourishChildAssentManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(
            subject_identifier=subject_identifier)


class PreFlourishChildAssent(SiteModelMixin, NonUniqueSubjectIdentifierFieldMixin,
                             IdentityFieldsMixin, PersonalFieldsMixin, ReviewFieldsMixin,
                             VulnerabilityFieldsMixin, CitizenFieldsMixin,
                             VerificationFieldsMixin, BaseUuidModel):
    identity = IdentityField(
        verbose_name='Identity number',
        null=True,
        blank=True)

    identity_type = models.CharField(
        verbose_name='What type of identity number is this?',
        max_length=25,
        choices=CHILD_IDENTITY_TYPE,
        null=True,
        blank=True)

    confirm_identity = IdentityField(
        help_text='Retype the identity number',
        null=True,
        blank=True)

    remain_in_study = models.CharField(
        max_length=3,
        verbose_name=('Are you willing to continue the study when you reach 18'
                      ' years of age?'),
        choices=YES_NO,
    )

    hiv_testing = models.CharField(
        max_length=3,
        verbose_name=('Are you willing to be tested for HIV ?'),
        choices=YES_NO,
        help_text='If no, participant is not eligible.')

    preg_testing = models.CharField(
        max_length=3,
        verbose_name='Are you willing to undergo pregnancy testing? ',
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text='If ‘No’ ineligible for study participation')

    specimen_consent = models.CharField(
        max_length=3,
        verbose_name='Do you give us permission to use your blood samples for future '
                     'studies?',
        choices=YES_NO)

    consent_datetime = models.DateTimeField(
        verbose_name='Consent date and time',
        validators=[
            datetime_not_before_study_start,
            datetime_not_future])

    version = models.CharField(
        max_length=3)

    objects = PreFlourishChildAssentManager()

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if not self.version:
            self.version = self.latest_consent_version
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.subject_identifier}'

    def natural_key(self):
        return self.subject_identifier

    @property
    def pre_flourish_child_consent_cls(self):
        return django_apps.get_model(
            'pre_flourish.preflourishcaregiverchildconsent')

    @property
    def screening_identifier(self):
        try:
            child_consent = self.pre_flourish_child_consent_cls.objects.filter(
                subject_identifier=self.subject_identifier).latest('consent_datetime')
        except self.pre_flourish_child_consent_cls.DoesNotExist:
            return None
        else:
            return child_consent.subject_consent.screening_identifier

    @property
    def latest_consent_version(self):
        consent_version_cls = django_apps.get_model(
            'pre_flourish.pfconsentversion')
        version = None

        try:
            consent_version_obj = consent_version_cls.objects.get(
                screening_identifier=self.screening_identifier)
        except consent_version_cls.DoesNotExist:
            version = '1'
        else:
            version = getattr(
                consent_version_obj, 'child_version', consent_version_obj.version)
        return version

    class Meta:
        app_label = 'pre_flourish'
        verbose_name = 'Child Assent for Participation'
        verbose_name_plural = 'Child Assent for Participation'
        unique_together = (
            ('subject_identifier', 'version'),
            ('first_name', 'last_name', 'identity', 'version'),
            ('first_name', 'dob', 'initials', 'version'))

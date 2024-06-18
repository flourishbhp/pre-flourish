from django.apps import apps as django_apps
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_crypto_fields.fields import IdentityField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future, datetime_not_future
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import age, get_utcnow
from edc_consent.field_mixins import IdentityFieldsMixin
from edc_consent.field_mixins import PersonalFieldsMixin
from edc_consent.field_mixins import ReviewFieldsMixin, VerificationFieldsMixin
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_protocol.validators import datetime_not_before_study_start

from flourish_caregiver.choices import CHILD_IDENTITY_TYPE
from ..caregiver import PreFlourishConsent
from ..model_mixins import SearchSlugModelMixin
from ...constants import INFANT
from ...subject_identifier import PFInfantIdentifier

pre_flourish_config = django_apps.get_app_config('pre_flourish')


class PreFlourishCaregiverChildConsent(SiteModelMixin,
                                       NonUniqueSubjectIdentifierFieldMixin,
                                       IdentityFieldsMixin, ReviewFieldsMixin,
                                       PersonalFieldsMixin, VerificationFieldsMixin,
                                       SearchSlugModelMixin, BaseUuidModel):
    """Inline table for caregiver's children"""

    subject_consent = models.ForeignKey(
        PreFlourishConsent,
        on_delete=models.PROTECT)

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        blank=True,
        null=True,
        max_length=50)

    identity = IdentityField(
        verbose_name='Identity number',
        null=True,
        blank=True)

    confirm_identity = IdentityField(
        help_text='Retype the identity number',
        null=True,
        blank=True)

    identity_type = models.CharField(
        verbose_name='What type of identity number is this?',
        max_length=25,
        choices=CHILD_IDENTITY_TYPE,
        null=True,
        blank=True)

    child_dob = models.DateField(
        verbose_name="Date of birth",
        validators=[date_not_future, ], )

    child_test = models.CharField(
        verbose_name='Will you allow for HIV testing and counselling of '
                     'your Child',
        max_length=5,
        choices=YES_NO,
        help_text='If no, participant is not eligible.')

    child_remain_in_study = models.CharField(
        verbose_name='Is your child willing to remain in the study area until '
                     '2025?',
        max_length=5,
        choices=YES_NO,
        help_text='If no, participant is not eligible.')

    child_preg_test = models.CharField(
        verbose_name='If your child is female and will be 12 years or older '
                     'prior to 30-Jun-2025, will you allow the female child '
                     'to undergo pregnancy testing?',
        max_length=5,
        choices=YES_NO_NA,
        help_text='If no, participant is not eligible.')

    child_knows_status = models.CharField(
        verbose_name='If your child is ≥ 16 years, have they been told about '
                     'your HIV?',
        max_length=5,
        choices=YES_NO_NA,
        help_text='If no, participant is not eligible.')

    future_studies_contact = models.CharField(
        verbose_name=('Do you give us permission for us to contact you or your child'
                      ' for future studies?'),
        max_length=3,
        choices=YES_NO, )

    child_age_at_enrollment = models.DecimalField(
        decimal_places=2,
        max_digits=4)

    consent_datetime = models.DateTimeField(
        verbose_name='Consent date and time',
        validators=[
            datetime_not_before_study_start,
            datetime_not_future])

    caregiver_visit_count = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        blank=True,
        null=True)

    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    ineligibility = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
        editable=False)

    twin_triplet = models.BooleanField(
        default=False,
        editable=False)

    version = models.CharField(
        verbose_name='Consent version',
        max_length=10,
        help_text='See \'Consent Type\' for consent versions by period.',
        editable=False)

    def save(self, *args, **kwargs):
        self.child_age_at_enrollment = age(self.child_dob, get_utcnow()).years

        if not self.version:
            self.version = self.child_consent_version

        if not self.subject_identifier:
            self.subject_identifier = PFInfantIdentifier(
                maternal_identifier=self.subject_consent.subject_identifier,
                registration_status=self.registration_status,
                registration_datetime=self.consent_datetime,
                subject_type=INFANT,
                supplied_infant_suffix=self.child_subject_identifier_postfix).identifier
            self.subject_identifier = f'{self.subject_identifier}'

        return super().save(*args, **kwargs)

    @property
    def registration_status(self):
        return 'REGISTERED'

    @property
    def child_subject_identifier_postfix(self):
        if self.twin_triplet:
            twin_id = self.subject_consent.subject_identifier + '-'
            multiple_births = self.subject_consent.multiple_births
            if multiple_births == 'twins':
                twin_id += '25'
                if not self.check_child_identifier_exists(twin_id):
                    child_identifier_postfix = '25'
                else:
                    child_identifier_postfix = '35'
            elif multiple_births == 'triplets':
                twin_id += '36'
                if not self.check_child_identifier_exists(twin_id):
                    child_identifier_postfix = '36'
                else:
                    twin_id = self.subject_consent.subject_identifier + '-46'
                    if not self.check_child_identifier_exists(twin_id):
                        child_identifier_postfix = '46'
                    else:
                        child_identifier_postfix = '56'
        else:
            child_identifier_postfix = self.child_identifier_postfix_by_count
        return child_identifier_postfix

    @property
    def child_identifier_postfix_by_count(self):
        model_cls = django_apps.get_model(self._meta.label_lower)
        children_count = len(set(model_cls.objects.filter(
            subject_consent__subject_identifier=self.subject_consent.subject_identifier
        ).exclude(child_dob=self.child_dob, first_name=self.first_name).values_list(
            'subject_identifier', flat=True)))

        if not children_count:
            child_identifier_postfix = 10
        else:
            child_identifier_postfix = f'{(children_count + 5) * 10}'

        return child_identifier_postfix

    def check_child_identifier_exists(self, subject_identifier):
        model_cls = django_apps.get_model(self._meta.label_lower)
        return model_cls.objects.filter(
            subject_identifier=subject_identifier).exists()

    @property
    def child_consent_version(self):

        consent_version_cls = django_apps.get_model('pre_flourish.pfconsentversion')
        try:
            consent_version_obj = consent_version_cls.objects.get(
                screening_identifier=self.subject_consent.screening_identifier)
        except consent_version_cls.DoesNotExist:
            return None
        else:
            return consent_version_obj.child_version if (
                consent_version_obj.child_version) else (
                pre_flourish_config.child_consent_version)

    @property
    def child_dataset(self):
        return True

    class Meta:
        app_label = 'pre_flourish'
        verbose_name = 'Caregiver Consent On Behalf Of Child'
        verbose_name_plural = 'Caregiver Consent On Behalf Of Child'

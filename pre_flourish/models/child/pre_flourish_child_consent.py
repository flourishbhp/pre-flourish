from django import forms
from django.apps import apps as django_apps
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_crypto_fields.fields import FirstnameField, LastnameField
from django_crypto_fields.fields import IdentityField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future, date_not_future
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_consent.field_mixins import IdentityFieldsMixin
from edc_consent.field_mixins import PersonalFieldsMixin
from edc_consent.field_mixins import ReviewFieldsMixin, VerificationFieldsMixin
from edc_constants.choices import GENDER, YES_NO_NA, YES_NO
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_protocol.validators import datetime_not_before_study_start
from flourish_caregiver.choices import CHILD_IDENTITY_TYPE
from flourish_caregiver.subject_identifier import InfantIdentifier
from ...constants import INFANT
from ..caregiver import PreFlourishConsent
from edc_base.utils import age, get_utcnow

class PreFlourishCaregiverChildConsent(SiteModelMixin, NonUniqueSubjectIdentifierFieldMixin,
                            IdentityFieldsMixin, ReviewFieldsMixin,
                            PersonalFieldsMixin, VerificationFieldsMixin, BaseUuidModel):

    """Inline table for caregiver's children"""

    subject_consent = models.ForeignKey(
        PreFlourishConsent,
        on_delete=models.PROTECT)

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        blank=True,
        null=True,
        max_length=50)


    identity_type = models.CharField(
        verbose_name='What type of identity number is this?',
        max_length=25,
        choices=CHILD_IDENTITY_TYPE,
        null=True,
        blank=True)


    child_dob = models.DateField(
        verbose_name="Date of birth",
        validators=[date_not_future, ],)

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
        choices=YES_NO,)

    specimen_consent = models.CharField(
        verbose_name=('Do you give us permission for us to use your child\'s blood '
                      'samples for future studies?'),
        max_length=3,
        choices=YES_NO,)

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
    
    @property
    def registration_status(self):
        return 'REGISTERED'
    
    @property
    def child_subject_identifier_postfix(self):
        
        children_count = PreFlourishCaregiverChildConsent.objects.filter(
            subject_identifier__istartswith = self.subject_consent.subject_identifier
        ).count()
        
        child_identifier_postfix = 0
        
        if not children_count:
            child_identifier_postfix = 10
        else:
            child_identifier_postfix = f'{(children_count + 1) * 10}'
        
        return child_identifier_postfix
    
    def save(self, *args, **kwargs):

        self.child_age_at_enrollment = age(self.child_dob, get_utcnow()).years
        
        if not self.subject_identifier:
            self.subject_identifier = InfantIdentifier(
                    maternal_identifier=self.subject_consent.subject_identifier,
                    registration_status=self.registration_status,
                    registration_datetime=self.consent_datetime,
                    subject_type=INFANT,
                    supplied_infant_suffix=self.child_subject_identifier_postfix).identifier
                
        return super().save(*args, **kwargs)
    
    class Meta:
        app_label = 'pre_flourish'
        verbose_name = 'Caregiver Consent On Behalf Of Child'
        verbose_name_plural = 'Caregiver Consent On Behalf Of Child'
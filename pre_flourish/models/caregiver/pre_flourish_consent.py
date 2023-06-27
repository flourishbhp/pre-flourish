from django.apps import apps as django_apps
from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_consent.field_mixins import (
    CitizenFieldsMixin, VulnerabilityFieldsMixin)
from edc_consent.field_mixins import IdentityFieldsMixin
from edc_consent.field_mixins import PersonalFieldsMixin
from edc_consent.managers import ConsentManager
from edc_consent.model_mixins import ConsentModelMixin
from edc_constants.choices import GENDER, YES_NO, YES_NO_NA
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_registration.model_mixins import (
    UpdatesOrCreatesRegistrationModelMixin)
from edc_search.model_mixins import SearchSlugManager

import pre_flourish.models
from .eligibility import ConsentEligibility
from .model_mixins import ReviewFieldsMixin, SearchSlugModelMixin
from ...choices import IDENTITY_TYPE, RECRUIT_CLINIC, RECRUIT_SOURCE
from ...subject_identifier import SubjectIdentifier


class SubjectConsentManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, subject_identifier, version):
        return self.get(
            subject_identifier=subject_identifier, version=version)


class PreFlourishConsent(
        ConsentModelMixin, SiteModelMixin,
        UpdatesOrCreatesRegistrationModelMixin,
        NonUniqueSubjectIdentifierModelMixin, IdentityFieldsMixin,
        ReviewFieldsMixin, PersonalFieldsMixin, CitizenFieldsMixin,
        VulnerabilityFieldsMixin, SearchSlugModelMixin, BaseUuidModel):

    """ A model completed by the user on the mother's consent. """

    subject_screening_model = 'flourish_caregiver.subjectscreening'

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        null=True)

    screening_identifier = models.CharField(
        verbose_name='Screening identifier',
        max_length=50)

    gender = models.CharField(
        verbose_name='Gender',
        choices=GENDER,
        max_length=1, )

    identity_type = models.CharField(
        verbose_name='What type of identity number is this?',
        max_length=25,
        choices=IDENTITY_TYPE)

    recruit_source = models.CharField(
        max_length=75,
        choices=RECRUIT_SOURCE,
        verbose_name="The caregiver first learned about the flourish "
                     "study from ")

    recruit_source_other = OtherCharField(
        max_length=35,
        verbose_name="if other recruitment source, specify...",
        blank=True,
        null=True)

    recruitment_clinic = models.CharField(
        max_length=100,
        verbose_name="The caregiver was recruited from",
        choices=RECRUIT_CLINIC)

    recruitment_clinic_other = models.CharField(
        max_length=100,
        verbose_name="if other recruitment, specify...",
        blank=True,
        null=True, )

    biological_caregiver = models.CharField(
        max_length=3,
        verbose_name='Are you the biological mother to the child or children?',
        choices=YES_NO)

    future_contact = models.CharField(
        max_length=3,
        verbose_name='Do you give us permission to be contacted for future studies?',
        choices=YES_NO)

    child_consent = models.CharField(
        max_length=3,
        verbose_name='Are you willing to consent for your child’s participation in '
                     'FLOURISH?',
        choices=YES_NO_NA,
        help_text='If ‘No’ ineligible for study participation')

    ineligibility = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
        editable=False)

    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    objects = SubjectConsentManager()

    consent = ConsentManager()

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.subject_identifier} V{self.version}'

    def save(self, *args, **kwargs):
        eligibility_criteria = ConsentEligibility(
            self.consent_reviewed, self.study_questions, self.assessment_score,
            self.consent_signature, self.consent_copy, self.child_consent)
        self.is_eligible = eligibility_criteria.is_eligible
        self.ineligibility = eligibility_criteria.error_message
        self.version = '1'
        if self.is_eligible:
            if self.created and not self.subject_identifier:
                self.subject_identifier = self.update_subject_identifier_on_save()
        super().save(*args, **kwargs)

    def natural_key(self):
        return self.subject_identifier, self.version

    @property
    def caregiver_type(self):
        """Return the letter that represents the caregiver type.
        """
        if self.biological_caregiver == 'Yes':
            return 'B'
        elif self.biological_caregiver == 'No':
            return 'C'
        return None

    def make_new_identifier(self):
        """Returns a new and unique identifier.

        Override this if needed.
        """
        if not self.is_eligible:
            return None
        subject_identifier = SubjectIdentifier(
            caregiver_type=self.caregiver_type,
            identifier_type='subject',
            requesting_model=self._meta.label_lower,
            site=self.site)
        return subject_identifier.identifier

    @property
    def consent_version(self):
        return self.version

    def registration_update_or_create(self):
        """Creates or Updates the registration model with attributes
        from this instance.

        Called from the signal
        """
        if self.is_eligible:
            return super().registration_update_or_create()

    @property
    def registration_model(self):
        return django_apps.get_model('pre_flourish.preflourishregisteredsubject')

    @property
    def registered_subject_model_class(self):
        """Returns the registered subject model class.
        """
        return django_apps.get_model('pre_flourish.preflourishregisteredsubject')

    class Meta(ConsentModelMixin.Meta):
        app_label = 'pre_flourish'
        verbose_name = 'Caregiver Consent'
        verbose_name_plural = 'Caregiver Consent'
        unique_together = (('subject_identifier', 'version'),
                           ('subject_identifier', 'screening_identifier', 'version'),
                           ('first_name', 'dob', 'initials', 'version'))

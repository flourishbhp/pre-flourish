from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_consent.field_mixins import IdentityFieldsMixin, CitizenFieldsMixin
from edc_consent.field_mixins import (PersonalFieldsMixin, ReviewFieldsMixin,
                                      VulnerabilityFieldsMixin)
from edc_consent.managers import ConsentManager
from edc_consent.model_mixins import ConsentModelMixin
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_registration.model_mixins import (
    UpdatesOrCreatesRegistrationModelMixin)
from edc_search.model_mixins import SearchSlugManager

from .eligibility import ConsentEligibility
from .model_mixins import SearchSlugModelMixin


class CaregiverChildScreeningConsentManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, subject_identifier, version):
        return self.get(
            subject_identifier=subject_identifier, version=version)


class CaregiverChildScreeningConsent(
        ConsentModelMixin, SiteModelMixin,
        UpdatesOrCreatesRegistrationModelMixin,
        NonUniqueSubjectIdentifierModelMixin, IdentityFieldsMixin,
        ReviewFieldsMixin, PersonalFieldsMixin,
        VulnerabilityFieldsMixin, CitizenFieldsMixin,
        SearchSlugModelMixin, BaseUuidModel):

    screening_identifier = models.CharField(
        verbose_name='Screening identifier',
        max_length=50)

    consent = ConsentManager()

    history = HistoricalRecords()

    objects = CaregiverChildScreeningConsentManager()

    def __str__(self):
        return f'{self.subject_identifier} V{self.version}'

    def save(self, *args, **kwargs):
        eligibility_criteria = ConsentEligibility(
            self.consent_reviewed, self.study_questions, self.assessment_score,
            self.consent_signature, self.consent_copy)
        self.is_eligible = eligibility_criteria.is_eligible
        self.ineligibility = eligibility_criteria.error_message
        self.version = '1'
        super().save(*args, **kwargs)

    def natural_key(self):
        return (self.subject_identifier, self.version)

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.extend(['identity', 'screening_identifier',
                       'first_name', 'last_name'])
        return fields

    class Meta(ConsentModelMixin.Meta):
        app_label = 'pre_flourish'
        verbose_name = 'Consent of Caregiver for Child/Adolescent Screening Participation'
        verbose_name_plural = 'Consent of Caregiver for Child/Adolescent Screening Participation'
        unique_together = (('subject_identifier', 'version'),
                           ('subject_identifier', 'screening_identifier', 'version'),
                           ('first_name', 'dob', 'initials', 'version'))

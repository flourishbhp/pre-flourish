from django.apps import apps as django_apps
from django.db import models
from django_crypto_fields.fields import IdentityField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_consent.model_mixins import ConsentModelMixin
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_registration.model_mixins import (
    UpdatesOrCreatesRegistrationModelMixin)
from edc_search.model_mixins import SearchSlugManager


class ChildDummySubjectConsentManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, subject_identifier, version):
        return self.get(
            subject_identifier=subject_identifier, version=version)


class PreFlourishChildDummySubjectConsent(
    ConsentModelMixin, UpdatesOrCreatesRegistrationModelMixin,
    SiteModelMixin, NonUniqueSubjectIdentifierFieldMixin, BaseUuidModel):
    """ A dummy child model auto completed by the s. """

    consent_datetime = models.DateTimeField(
        verbose_name='Consent date and time', )

    report_datetime = models.DateTimeField(
        null=True,
        editable=False,
        default=get_utcnow)

    identity = IdentityField(
        verbose_name='Identity number',
        null=True)

    dob = models.DateField(
        verbose_name="Date of birth",
        null=True,
        blank=False)

    history = HistoricalRecords()

    objects = ChildDummySubjectConsentManager()

    def save(self, *args, **kwargs):
        self.relative_identifier = self.subject_identifier[:-3]
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.subject_identifier}'

    def natural_key(self):
        return self.subject_identifier

    @property
    def registration_model(self):
        return django_apps.get_model('pre_flourish.preflourishregisteredsubject')

    class Meta(ConsentModelMixin.Meta):
        app_label = 'pre_flourish'
        verbose_name = 'Child Dummy Subject Consent'
        unique_together = ()

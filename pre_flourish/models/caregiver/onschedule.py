from django.apps import apps as django_apps
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager
from edc_identifier.managers import SubjectIdentifierManager
from edc_visit_schedule.model_mixins import \
    OnScheduleModelMixin as BaseOnScheduleModelMixin

pre_flourish_config = django_apps.get_app_config('pre_flourish')


class OnScheduleModelMixin(BaseOnScheduleModelMixin, BaseUuidModel):
    """A model used by the system. Auto-completed by enrollment model.
    """

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50)

    child_subject_identifier = models.CharField(
        verbose_name="Associated Child Identifier",
        max_length=50)

    schedule_name = models.CharField(max_length=25, blank=True, null=True)

    on_site = CurrentSiteManager()

    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    def put_on_schedule(self):
        pass

    def save(self, *args, **kwargs):
        self.consent_version = self.get_version
        super().save(*args, **kwargs)

    @property
    def consent_version_model(self):
        return django_apps.get_model('pre_flourish', 'PFConsentVersion')

    @property
    def subject_consent_model(self):
        return django_apps.get_model('pre_flourish', 'PreFlourishConsent')

    @property
    def get_version(self):
        version = None
        try:
            consent_version_obj = self.consent_version_model.objects.get(
                screening_identifier=self.screening_identifier,
                version=str(pre_flourish_config.consent_version)
            )
        except self.consent_version_model.DoesNotExist:
            version = '1'
        else:
            version = consent_version_obj.version
        return version

    @property
    def screening_identifier(self):
        try:
            return self.subject_consent_model.objects.filter(
                subject_identifier=self.subject_identifier,
            ).latest('consent_datetime').screening_identifier
        except self.subject_consent_model.DoesNotExist:
            pass

    class Meta:
        unique_together = ('subject_identifier', 'schedule_name')
        abstract = True


class OnSchedulePreFlourish(OnScheduleModelMixin):
    pass


class OnScheduleChildPreFlourish(OnScheduleModelMixin):
    pass

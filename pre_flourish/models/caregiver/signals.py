from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_base import get_utcnow
from edc_constants.constants import NO
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from pre_flourish.helper_classes.utils import update_worklist
from .pre_flourish_consent import PreFlourishConsent
from .pre_flourish_subject_screening import PreFlourishSubjectScreening
from ..child.pre_flourish_child_assent import PreFlourishChildAssent

pre_flourish_config = django_apps.get_app_config('pre_flourish')


class PreFlourishSubjectScreeningError(Exception):
    pass


def update_locator(consent, screening):
    locator_model = 'flourish_caregiver.caregiverlocator'
    locator_cls = django_apps.get_model(locator_model)
    try:
        locator_obj = locator_cls.objects.get(
            study_maternal_identifier=screening.study_maternal_identifier
        )
    except locator_cls.DoesNotExist:
        pass
    else:
        locator_obj.screening_identifier = getattr(
            screening, 'screening_identifier', None)
        if consent:
            locator_obj.subject_identifier = getattr(
                consent, 'subject_identifier', None)
        is_bio_mother = getattr(consent, 'biological_caregiver', None)
        if is_bio_mother == NO:
            locator_obj.first_name = getattr(consent, 'first_name', None)
            locator_obj.last_name = getattr(consent, 'last_name', None)
        locator_obj.save()


@receiver(post_save, weak=False, sender=PreFlourishConsent,
          dispatch_uid='pre_flourish_consent_on_post_save')
def pre_flourish_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """ Updates locator instance with subject and screening identifier once consented.
    """
    if not raw and instance.is_eligible:
        try:
            caregiver_screening = PreFlourishSubjectScreening.objects.get(
                screening_identifier=instance.screening_identifier)
        except PreFlourishSubjectScreening.DoesNotExist:
            raise PreFlourishSubjectScreeningError(
                'Missing PreFlourishSubjectScreening form.')
        else:
            caregiver_screening.subject_identifier = instance.subject_identifier
            caregiver_screening.is_consented = True
            caregiver_screening.has_passed_consent = True
            caregiver_screening.save()

            update_locator(consent=instance, screening=caregiver_screening)
            update_worklist(caregiver_screening.study_maternal_identifier)
            create_consent_version(instance, instance.version)


@receiver(post_save, weak=False, sender=PreFlourishSubjectScreening,
          dispatch_uid='pre_flourish_screening_on_post_save')
def pre_flourish_screening_on_post_save(sender, instance, raw, created, **kwargs):
    """ Updates screening identifier to locator model once successfully screened.
    """
    if not raw and instance.is_eligible:
        update_locator(consent=None, screening=instance)


@receiver(post_save, weak=False, sender=PreFlourishChildAssent,
          dispatch_uid='pre_flourish_assent_post_save')
def pre_flourish_assent_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        # get caregiver's consent
        try:
            caregiver_consent = PreFlourishConsent.objects.filter(
                subject_identifier=instance.subject_identifier[:-3]).latest(
                'consent_datetime'
            )
        except PreFlourishConsent.DoesNotExist:
            raise ValidationError("Missing caregiver consent")
        else:
            put_on_schedule(caregiver_consent,
                            caregiver_consent.subject_identifier,
                            'pre_flourish.onschedulepreflourish',
                            'pre_flourish_schedule1',
                            child_subject_identifier=instance.subject_identifier, )


def put_on_schedule(instance, subject_identifier,
                    onschedule_model, schedule_name, child_subject_identifier=None):
    if instance:
        subject_identifier = subject_identifier or instance.subject_identifier

        _, schedule = site_visit_schedules.get_by_onschedule_model(
            onschedule_model)

        onschedule_model_cls = django_apps.get_model(onschedule_model)

        try:
            onschedule_model_cls.objects.get(
                subject_identifier=instance.subject_identifier,
                child_subject_identifier=child_subject_identifier,
                schedule_name=schedule_name)
        except onschedule_model_cls.DoesNotExist:
            schedule.put_on_schedule(
                subject_identifier=instance.subject_identifier,
                onschedule_datetime=instance.created.replace(microsecond=0),
                schedule_name=schedule_name)
        else:
            try:
                onschedule_obj = schedule.onschedule_model_cls.objects.get(
                    subject_identifier=subject_identifier,
                    schedule_name=schedule_name,
                    child_subject_identifier='')
            except schedule.onschedule_model_cls.DoesNotExist:
                schedule.refresh_schedule(
                    subject_identifier=instance.subject_identifier,
                    schedule_name=schedule_name)
            else:
                onschedule_obj.child_subject_identifier = child_subject_identifier
                onschedule_obj.save()


def create_consent_version(instance, version, child_version=None):
    consent_version_cls = django_apps.get_model(
        'pre_flourish.pfconsentversion')

    try:
        consent_version_cls.objects.get(
            screening_identifier=instance.screening_identifier)
    except consent_version_cls.DoesNotExist:
        consent_version = consent_version_cls(
            screening_identifier=instance.screening_identifier,
            version=version,
            child_version=child_version,
            user_created=instance.user_modified or instance.user_created,
            created=get_utcnow())
        consent_version.save()

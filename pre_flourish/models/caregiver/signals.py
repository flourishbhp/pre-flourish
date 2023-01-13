from django.apps import apps as django_apps
from django.db.models.signals import post_save
from django.dispatch import receiver

from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from .pre_flourish_consent import PreFlourishConsent
from .pre_flourish_subject_screening import PreFlourishSubjectScreening


class PreFlourishSubjectScreeningError(Exception):
    pass


@receiver(post_save, weak=False, sender=PreFlourishConsent,
          dispatch_uid='pre_flourish_consent_on_post_save')
def pre_flourish_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """Creates an onschedule instance for this enrolled subject.
    """
    if not raw:
        try:
            caregiver_screening = PreFlourishSubjectScreening.objects.get(
                screening_identifier=instance.screening_identifier)
        except PreFlourishSubjectScreening.DoesNotExist:
            raise PreFlourishSubjectScreeningError(
                'Missing PreFlourishSubjectScreening form.')
        else:
            caregiver_screening.is_consented = True
            caregiver_screening.save()

        if instance.is_eligible:
            if caregiver_screening:
                caregiver_screening.has_passed_consent = True
                caregiver_screening.subject_identifier = instance.subject_identifier
                caregiver_screening.save()

            put_on_schedule(instance, instance.subject_identifier,
                            'pre_flourish.onschedulepreflourish',
                            'pre_flourish_schedule1')


def put_on_schedule(instance, subject_identifier,
                    onschedule_model, schedule_name):
    if instance:
        subject_identifier = subject_identifier or instance.subject_identifier

        _, schedule = site_visit_schedules.get_by_onschedule_model(
            onschedule_model)

        onschedule_model_cls = django_apps.get_model(onschedule_model)

        try:
            onschedule_model_cls.objects.get(
                subject_identifier=instance.subject_identifier,
                schedule_name=schedule_name)
        except onschedule_model_cls.DoesNotExist:
            schedule.put_on_schedule(
                subject_identifier=instance.subject_identifier,
                onschedule_datetime=instance.created,
                schedule_name=schedule_name)
        else:
            schedule.refresh_schedule(
                subject_identifier=instance.subject_identifier,
                schedule_name=schedule_name)

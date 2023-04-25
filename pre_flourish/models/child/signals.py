from django.apps import apps as django_apps
from django.db.models.signals import post_save
from django.dispatch import receiver

from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from pre_flourish.models.child import PreFlourishChildDummySubjectConsent
from pre_flourish.models.child import PreFlourishChildAssent
from pre_flourish.models.child import PreFlourishCaregiverChildConsent


class CaregiverConsentError(Exception):
    pass




@receiver(post_save, weak=False, sender=PreFlourishChildAssent,
          dispatch_uid='pre_flourish_child_assent_on_post_save')
def child_assent_on_post_save(sender, instance, raw, created, **kwargs):
    """Put subject on schedule after consenting.
    """
    if not raw:
        caregiver_child_consent_cls = django_apps.get_model(
            'pre_flourish.preflourishcaregiverchildconsent')
        try:
            caregiver_child_consent_obj = caregiver_child_consent_cls.objects.get(
                subject_identifier=instance.subject_identifier, )
        except caregiver_child_consent_cls.DoesNotExist:
            raise CaregiverConsentError('Associated caregiver consent on behalf of '
                                        'child for this participant not found')
        else:
            create_child_dummy_consent(instance, caregiver_child_consent_obj)


@receiver(post_save, weak=False, sender=PreFlourishChildDummySubjectConsent,
          dispatch_uid='pre_flourish_child_dummy_consent_on_post_save')
def pre_flourish_child_dummy_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """Put subject on schedule after consenting.
    """
    if not raw:
        put_on_schedule(
            subject_identifier=instance.subject_identifier,
            onschedule_model='pre_flourish.onschedulechildpreflourish',
            schedule_name='pf_child_schedule1',
            base_appt_datetime=instance.consent_datetime
        )


def create_child_dummy_consent(instance, caregiver_child_consent_obj=None):
    caregiver_child_consent_obj = caregiver_child_consent_obj or instance
    try:
        PreFlourishChildDummySubjectConsent.objects.get(
            subject_identifier=instance.subject_identifier)
    except PreFlourishChildDummySubjectConsent.DoesNotExist:
        PreFlourishChildDummySubjectConsent.objects.create(
            subject_identifier=caregiver_child_consent_obj.subject_identifier,
            consent_datetime=caregiver_child_consent_obj.consent_datetime,
            identity=caregiver_child_consent_obj.identity,
            dob=caregiver_child_consent_obj.dob,
        )


def put_on_schedule(instance=None, subject_identifier=None,
                    base_appt_datetime=None, onschedule_model=None, schedule_name=None):
    _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
        onschedule_model=onschedule_model, name=schedule_name)

    schedule.put_on_schedule(
        subject_identifier=subject_identifier,
        onschedule_datetime=base_appt_datetime,
        schedule_name=schedule_name,
        base_appt_datetime=base_appt_datetime)

from django.apps import apps as django_apps
from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_base import get_utcnow
from edc_visit_schedule import site_visit_schedules

from pre_flourish.helper_classes.heu_huu_matching_helper import HEUHUUMatchingHelper
from pre_flourish.models.child.pre_flourish_child_dummy_consent import \
    PreFlourishChildDummySubjectConsent
from pre_flourish.models.child.heu_huu_match import HeuHuuMatch
from pre_flourish.models.child.huu_pre_enrollment import HuuPreEnrollment
from pre_flourish.models.child.pre_flourish_child_assent import PreFlourishChildAssent


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
def pre_flourish_child_dummy_consent_on_post_save(sender, instance, raw, created,
                                                  **kwargs):
    """Put subject on schedule after consenting.
    """
    if not raw:
        put_on_schedule(
            subject_identifier=instance.subject_identifier,
            onschedule_model='pre_flourish.onschedulechildpreflourish',
            schedule_name='pf_child_schedule1',
            base_appt_datetime=instance.consent_datetime
        )


@receiver(post_save, weak=False, sender=HuuPreEnrollment,
          dispatch_uid='huu_pre_enrollment_on_post_save')
def huu_pre_enrollment_on_post_save(sender, instance, raw, created, **kwargs):
    """Create a HEUHUUMatch object when a HuuPreEnrollment object is saved.

    This function is called after a HuuPreEnrollment object is saved to the database.
    If the object is not newly created, the function fetches a related
    PreFlourishChildAssent object from the database. If the related object is found,
    the function creates a new HeuHuuMatch object and saves it to the database.

    Args:
        sender: The model class of the sender.
        instance: The actual instance being saved.
        raw: A boolean indicating whether the model is saved in raw mode.
        created: A boolean indicating whether the model was created or updated.
        **kwargs: Additional keyword arguments.

    Raises:
        CaregiverConsentError: If the associated caregiver consent on behalf of the child
            for this participant is not found.

    Returns:
        None
    """
    if not raw:
        pre_flourish_child_assent_cls = django_apps.get_model(
            'pre_flourish.preflourishchildassent')
        try:
            pre_flourish_child_assent_obj = pre_flourish_child_assent_cls.objects.get(
                subject_identifier=instance.pre_flourish_visit.subject_identifier, )
        except pre_flourish_child_assent_cls.DoesNotExist:
            raise CaregiverConsentError('Associated caregiver consent on behalf of '
                                        'child for this participant not found')
        else:
            heu_huu_matching_helper = HEUHUUMatchingHelper(
                dob=pre_flourish_child_assent_obj.dob,
                child_weight_kg=instance.weight,
                child_height_cm=instance.height,
                subject_identifier=instance.pre_flourish_visit.subject_identifier,
                gender=pre_flourish_child_assent_obj.gender)
            heu_subject_identifier = heu_huu_matching_helper.find_matching_flourish()
            if heu_subject_identifier:
                try:
                    HeuHuuMatch.objects.get(
                        huu_prt=instance.pre_flourish_visit.subject_identifier,
                        heu_prt=heu_subject_identifier.get('subject_identifier'))
                except HeuHuuMatch.DoesNotExist:
                    heu_huu_match_obj = HeuHuuMatch.objects.create(
                        huu_prt=instance.pre_flourish_visit.subject_identifier,
                        heu_prt=heu_subject_identifier.get('subject_identifier'),
                        match_datetime=get_utcnow().date()
                    )
                    heu_huu_match_obj.save()


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


def put_on_schedule(subject_identifier=None, base_appt_datetime=None,
                    onschedule_model=None, schedule_name=None):
    _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
        onschedule_model=onschedule_model, name=schedule_name)

    schedule.put_on_schedule(
        subject_identifier=subject_identifier,
        onschedule_datetime=base_appt_datetime,
        schedule_name=schedule_name,
        base_appt_datetime=base_appt_datetime)

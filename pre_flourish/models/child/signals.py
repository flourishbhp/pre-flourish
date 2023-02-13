from django.apps import apps as django_apps
from django.db.models.signals import post_save
from django.dispatch import receiver

from flourish_child.models import ChildDummySubjectConsent
from pre_flourish.models.child.pre_flourish_child_assent import PreFlourishChildAssent
from pre_flourish.models.child.pre_flourish_child_consent import \
    PreFlourishCaregiverChildConsent


class CaregiverConsentError(Exception):
    pass


@receiver(post_save, weak=False, sender=PreFlourishCaregiverChildConsent,
          dispatch_uid='pre_flourish_caregiver_child_consent_on_post_save')
def pre_flourish_caregiver_child_consent_on_post_save(sender, instance, raw, created,
        **kwargs):
    if not raw and instance.is_eligible:
        create_child_dummy_consent(instance)


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
            if caregiver_child_consent_obj.is_eligible:
                create_child_dummy_consent(instance, caregiver_child_consent_obj)


def create_child_dummy_consent(instance, caregiver_child_consent_obj=None):
    caregiver_child_consent_obj = caregiver_child_consent_obj or instance
    try:
        ChildDummySubjectConsent.objects.get(
            subject_identifier=instance.subject_identifier)
    except ChildDummySubjectConsent.DoesNotExist:
        ChildDummySubjectConsent.objects.create(
            subject_identifier=instance.subject_identifier,
            consent_datetime=instance.consent_datetime,
            identity=instance.identity,
            dob=instance.dob,
            cohort=caregiver_child_consent_obj.cohort, )

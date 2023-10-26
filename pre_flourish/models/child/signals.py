from django.apps import apps as django_apps
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from dateutil.relativedelta import relativedelta
from edc_action_item import site_action_items
from edc_base import get_utcnow
from edc_base.utils import age
from edc_constants.constants import NEG, NEW, OPEN, POS
from edc_visit_schedule import site_visit_schedules

from pre_flourish.action_items import CHILD_OFF_STUDY_ACTION
from pre_flourish.helper_classes.utils import create_child_dummy_consent, \
    get_or_create_caregiver_dataset, \
    get_or_create_child_dataset, pre_flourish_caregiver_child_consent, \
    put_on_schedule, trigger_action_item
from pre_flourish.models.child import HuuPreEnrollment, PreFlourishChildAssent, \
    PreFlourishChildDummySubjectConsent


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
          dispatch_uid='huu_pre_enrollment_post_save')
def huu_pre_enrollment_post_save(sender, instance, raw, created, **kwargs):
    child_off_study_cls = django_apps.get_model('pre_flourish.preflourishchildoffstudy')
    if not raw:
        if instance.child_hiv_result == POS:
            trigger_action_item(
                model_cls=child_off_study_cls,
                action_name=CHILD_OFF_STUDY_ACTION,
                subject_identifier=instance.subject_identifier,
            )

        current_date = get_utcnow().date()

        child_test_date = instance.child_test_date

        three_months_ago = current_date - relativedelta(months=3)

        # check if the child was tested within three months from now
        # child_test_date is when the child was tested
        within_three_months = three_months_ago <= child_test_date <= current_date

        if instance.child_hiv_result == NEG and within_three_months:
            caregiver_child_consent = pre_flourish_caregiver_child_consent(instance)
            get_or_create_caregiver_dataset(caregiver_child_consent.subject_consent)
            get_or_create_child_dataset(caregiver_child_consent)


def trigger_action_item(model_cls, action_name, subject_identifier,
                        repeat=False, opt_trigger=True):
    action_cls = site_action_items.get(
        model_cls.action_name)
    action_item_model_cls = action_cls.action_item_model_cls()

    try:
        model_cls.objects.get(subject_identifier=subject_identifier)
    except model_cls.DoesNotExist:
        trigger = opt_trigger and True
    else:
        trigger = repeat

    if trigger:
        try:
            action_item_obj = action_item_model_cls.objects.get(
                subject_identifier=subject_identifier,
                action_type__name=action_name)
        except action_item_model_cls.DoesNotExist:
            action_cls = site_action_items.get(action_name)
            action_cls(subject_identifier=subject_identifier)
        else:
            action_item_obj.status = OPEN
            action_item_obj.save()
    else:
        try:
            action_item = action_item_model_cls.objects.get(
                Q(status=NEW) | Q(status=OPEN),
                subject_identifier=subject_identifier,
                action_type__name=action_name)
        except action_item_model_cls.DoesNotExist:
            pass
        else:
            action_item.delete()


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
        onschedule_datetime=base_appt_datetime.replace(microsecond=0),
        schedule_name=schedule_name,
        base_appt_datetime=base_appt_datetime.replace(microsecond=0))

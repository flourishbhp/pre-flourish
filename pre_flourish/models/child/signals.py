from cacheops import invalidate_obj
from django.apps import apps as django_apps
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_action_item import site_action_items
from edc_base import get_utcnow
from edc_constants.constants import NEG, NEW, OPEN, POS
from edc_visit_schedule import site_visit_schedules

from pre_flourish.action_items import CHILD_OFF_STUDY_ACTION
from pre_flourish.helper_classes import MatchHelper
from pre_flourish.helper_classes.utils import create_child_dummy_consent, \
    date_within_specific_months, get_or_create_caregiver_dataset, \
    get_or_create_child_dataset, pre_flourish_caregiver_child_consent, put_on_schedule, \
    trigger_action_item
from pre_flourish.models.child import HuuPreEnrollment, PFChildHIVRapidTestCounseling, \
    PreFlourishChildAssent, PreFlourishChildDummySubjectConsent
from ...models.contact_proxy import PreFlourishContact


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
            caregiver_child_consent_obj = caregiver_child_consent_cls.objects.filter(
                subject_identifier=instance.subject_identifier, ).latest(
                'consent_datetime')
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

        if instance.child_test_date:

            current_date = get_utcnow().date()

            child_test_date = instance.child_test_date

            within_three_months = date_within_specific_months(child_test_date,
                                                              current_date, 3)

            if instance.child_hiv_result == NEG and within_three_months:
                match_helper = MatchHelper()
                caregiver_child_consent = pre_flourish_caregiver_child_consent(instance)
                get_or_create_caregiver_dataset(caregiver_child_consent.subject_consent)
                get_or_create_child_dataset(caregiver_child_consent)
                match_helper.update_metrix(instance)


@receiver(post_save, weak=False, sender=PFChildHIVRapidTestCounseling,
          dispatch_uid='pf_child_hiv_rapid_test_counseling_post_save')
def pf_child_hiv_rapid_test_counseling_post_save(sender, instance, raw, created,
                                                 **kwargs):
    if not raw and instance.rapid_test_done:

        current_date = get_utcnow().date()

        result_date = instance.result_date

        # check if the child was tested within three months from now
        # child_test_date is when the child was tested
        within_three_months = date_within_specific_months(result_date, current_date, 3)

        if instance.result == NEG and within_three_months:
            caregiver_child_consent = pre_flourish_caregiver_child_consent(instance)
            get_or_create_caregiver_dataset(caregiver_child_consent.subject_consent)
            get_or_create_child_dataset(caregiver_child_consent)


@receiver(post_save, weak=False, sender=PreFlourishContact,
          dispatch_uid='pre_flourish_contact_post_save')
def pre_flourish_contact_post_save(sender, instance, raw, created, **kwargs):
    participant_note_cls = django_apps.get_model('flourish_calendar.participantnote')

    if not raw:
        if getattr(instance, 'appt_date', None):
            obj, _created = participant_note_cls.objects.update_or_create(
                subject_identifier=instance.subject_identifier,
                title='PF to Flourish Enrol',
                defaults={'date': instance.appt_date,
                          'description': 'Pre-flourish contact for flourish enrolment scheduling.',})
            if not _created:
                invalidate_obj(obj)


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
            version=caregiver_child_consent_obj.version,
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

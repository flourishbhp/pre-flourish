from celery.app import shared_task
from django.db.models import Q
from edc_action_item import site_action_items
from edc_constants.constants import FEMALE, MALE, NEG, NEW, NO, OPEN
from edc_visit_schedule import site_visit_schedules

from flourish_caregiver.models import MaternalDataset
from flourish_child.models import ChildDataset
from pre_flourish.helper_classes.heu_pool_generation import HEUPoolGeneration
from pre_flourish.helper_classes.huu_pool_generation import HUUPoolGeneration
from pre_flourish.models.caregiver.pre_flourish_subject_screening import \
    PreFlourishSubjectScreening
from pre_flourish.models.child.pre_flourish_child_consent import \
    PreFlourishCaregiverChildConsent
from pre_flourish.models.child.pre_flourish_child_dummy_consent import \
    PreFlourishChildDummySubjectConsent


def get_or_create_caregiver_dataset(consent):
    defaults = {
        'protocol': 'BCPP',
        'screening_identifier': consent.screening_identifier,
    }
    if 'B' in consent.subject_identifier:
        defaults.update({
            'first_name': consent.first_name,
            'last_name': consent.last_name,
        })
    obj, _ = MaternalDataset.objects.update_or_create(
        defaults=defaults,
        study_maternal_identifier=pre_flourish_screening_obj(
            consent.screening_identifier).study_maternal_identifier)
    return obj


def get_or_create_child_dataset(consent):
    genders = {MALE: 'Male', FEMALE: 'Female'}
    defaults = {
        'first_name': consent.first_name,
        'last_name': consent.last_name,
        'dob': consent.child_dob,
        'infant_sex': genders.get(consent.gender),
        'infant_hiv_exposed': 'Unexposed',
        'infant_hiv_status': NEG,
        'infant_breastfed': NO,
        'infant_enrolldate': consent.consent_datetime,
        'study_maternal_identifier': pre_flourish_screening_obj(
            consent.subject_consent.screening_identifier).study_maternal_identifier,
        'age_gt17_5': 1,
        'infant_offstudy_complete': 1,
        'infant_offstudy_reason': 'Completion of protocol',
        'infant_vitalstatus_final': 'Alive'
    }
    ChildDataset.objects.update_or_create(
        defaults=defaults,
        study_child_identifier=consent.subject_identifier)


def pre_flourish_screening_obj(screening_identifier):
    try:
        return PreFlourishSubjectScreening.objects.get(
            screening_identifier=screening_identifier
        )
    except PreFlourishCaregiverChildConsent.DoesNotExist:
        raise


def pre_flourish_caregiver_child_consent(instance):
    try:
        return PreFlourishCaregiverChildConsent.objects.get(
            subject_identifier=instance.subject_identifier
        )
    except PreFlourishCaregiverChildConsent.DoesNotExist:
        raise


def trigger_action_item(model_cls, action_name, subject_identifier,
                        repeat=False, opt_trigger=True):
    action_cls = site_action_items.get(model_cls.action_name)
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
        onschedule_datetime=base_appt_datetime,
        schedule_name=schedule_name,
        base_appt_datetime=base_appt_datetime)


@shared_task
def populate_heu_huu_pool_data():
    HUUPoolGeneration().generate_pool()
    HEUPoolGeneration().generate_pool()

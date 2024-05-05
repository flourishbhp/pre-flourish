import datetime

from celery.app import shared_task
from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.db.models import Q
from edc_action_item import site_action_items
from edc_base.utils import age, get_utcnow
from edc_constants.constants import FEMALE, MALE, NEG, NEW, NO, OPEN, POS
from edc_visit_schedule import site_visit_schedules

from flourish_caregiver.models.maternal_dataset import MaternalDataset
from flourish_child.models import ChildDataset
from pre_flourish.helper_classes.heu_pool_generation import HEUPoolGeneration
from pre_flourish.helper_classes.huu_pool_generation import HUUPoolGeneration
from pre_flourish.helper_classes.match_helper import MatchHelper
from pre_flourish.models.caregiver.pre_flourish_subject_screening import \
    PreFlourishSubjectScreening
from pre_flourish.models.child.pre_flourish_child_consent import \
    PreFlourishCaregiverChildConsent
from pre_flourish.models.child.pre_flourish_child_dummy_consent import \
    PreFlourishChildDummySubjectConsent


def huu_pre_enrollment_cls():
    return django_apps.get_model('pre_flourish.huupreenrollment')


def pre_flourish_child_consent_model_cls():
    return django_apps.get_model(
        'pre_flourish.preflourishcaregiverchildconsent')


def matrix_pool_cls():
    return django_apps.get_model('pre_flourish.matrixpool')


pre_flourish_config = django_apps.get_app_config('pre_flourish')
twin_triplet = {'twins': 2,
                'triplets': 3}


def get_or_create_caregiver_dataset(consent):
    defaults = {
        'protocol': 'BCPP',
        'screening_identifier': consent.screening_identifier,
        'twin_triplet': twin_triplet.get(consent.multiple_births, None)
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
        'infant_vitalstatus_final': 'Alive',
        'twin_triplet': consent.twin_triplet
    }
    ChildDataset.objects.update_or_create(
        defaults=defaults,
        study_child_identifier=consent.subject_identifier)


def pre_flourish_screening_obj(screening_identifier):
    try:
        return PreFlourishSubjectScreening.objects.get(
            screening_identifier=screening_identifier
        )
    except PreFlourishSubjectScreening.DoesNotExist:
        raise


def pre_flourish_caregiver_child_consent(instance):
    subject_identifier = instance if isinstance(instance, str) else instance.subject_identifier
    try:
        return PreFlourishCaregiverChildConsent.objects.filter(
            subject_identifier=subject_identifier
        ).latest('consent_datetime')
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


def date_within_specific_months(value, upper_bond, months=0):
    """
    Compare date if its within a lower_bond and upper bond, and should be type of date
    :param value: value of interest
    :param upper_bond: date limit
    :param months: offset months
    :return: return a true/false if the value with limits
    """

    lower_bond = value - relativedelta(months=months)

    if not isinstance(value, datetime.date):
        value = datetime.datetime.combine(value, datetime.datetime.min.time())

    return lower_bond <= value <= upper_bond


def pre_flourish_child_consent_model_objs(subject_identifier):
    return pre_flourish_child_consent_model_cls().objects.filter(
        subject_consent__subject_identifier=subject_identifier)


def latest_huu_pre_enrollment_objs(subject_identifier):
    latest_huu_pre_enrollment_objs = []

    for obj in pre_flourish_child_consent_model_objs(subject_identifier):
        huu_pre_enroll_obj = get_latest_huu_pre_enrollment_obj(obj.subject_identifier)
        if huu_pre_enroll_obj:
            latest_huu_pre_enrollment_objs.append(huu_pre_enroll_obj)
    return latest_huu_pre_enrollment_objs


def get_latest_huu_pre_enrollment_obj(subject_identifier):
    """ Returns the latest child HUU pre enrollment instance for a
        specific child subject_identifier.
    """
    try:
        huu_pre_enrollment_obj = huu_pre_enrollment_cls().objects.filter(
                pre_flourish_visit__subject_identifier=subject_identifier
            ).latest('report_datetime')
    except huu_pre_enrollment_cls().DoesNotExist:
        return None
    else:
        return huu_pre_enrollment_obj


def valid_by_age(subject_identifier):
    """ Returns True if child is valid by age i.e. age between 7 and 9.5 inclusive.
        @param subject_identifier: child subject_identifier
    """
    consent_obj = pre_flourish_caregiver_child_consent(subject_identifier)

    _age = age(consent_obj.child_dob, get_utcnow())
    _age = _age.years + (_age.months / 12)
    if 7 <= _age <= 9.5:
        return True


def child_is_hiv_pos(subject_identifier):
    """ Check if child's HIV test result is Positive, for eligibility
        @param subject_identifier: child subject_identifier
        @return: bool `True` if child is POS else `False`
    """
    huu_pre_enroll_obj = get_latest_huu_pre_enrollment_obj(subject_identifier)
    is_pos = getattr(huu_pre_enroll_obj, 'child_hiv_result', None) == POS
    return is_pos


def is_flourish_eligible(subject_identifier):
    """ Returns True if child subject is flourish eligible.
        @param subject_identifier: child subject_identifier
        @return: eligibility, message set
    """
    eligibility_message = 'This subject is eligible for Flourish Enrolment.'
    match_helper = MatchHelper()
    if child_is_hiv_pos(subject_identifier):
        return False, 'Child is HIV Positive, please complete off study form.'
    if valid_by_age(subject_identifier):
        return True, eligibility_message
    obj = get_latest_huu_pre_enrollment_obj(subject_identifier)

    if obj:
        bmi = obj.child_weight_kg / ((obj.child_height / 100) ** 2)
        bmi_group = match_helper.bmi_group(bmi)
        age_range = match_helper.age_range(obj.child_age)
        gender = 'male' if obj.gender == MALE else 'female'
        if bmi_group is None or age_range is None:
            pass
        if matrix_pool_cls().objects.filter(
                pool='heu', bmi_group=bmi_group, age_group=age_range,
                gender_group=gender, ).exists():
            return True, eligibility_message
    return None, None


def get_consent_version_obj(screening_identifier=None):
    consent_version_cls = django_apps.get_model('pre_flourish.pfconsentversion')
    try:
        return consent_version_cls.objects.get(
            screening_identifier=screening_identifier)
    except consent_version_cls.DoesNotExist:
        return None


def get_is_latest_consent_version(consent_version_obj):
    if not consent_version_obj:
        return False
    return str(consent_version_obj.version) == str(
        pre_flourish_config.consent_version)


def caregiver_subject_identifier(subject_identifier):
    subject_identifier = subject_identifier.split('-')
    subject_identifier.pop()
    caregiver_subject_identifier = '-'.join(subject_identifier)
    return caregiver_subject_identifier

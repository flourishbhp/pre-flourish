from dateutil.relativedelta import relativedelta
from edc_base.utils import get_utcnow
from edc_constants.constants import ALIVE, NOT_APPLICABLE, ON_STUDY, PARTICIPANT, YES
from edc_visit_tracking.constants import SCHEDULED
from faker import Faker
from model_mommy.recipe import Recipe, seq

from flourish_caregiver.models import CaregiverLocator, MaternalDataset, CohortSchedules
from flourish_child.models import ChildAssent
from .models import CyhuuPreEnrollment, HuuPreEnrollment, PFChildHIVRapidTestCounseling, \
    PFConsentVersion, PreFlourishCaregiverChildConsent, PreFlourishChildAssent, \
    PreFlourishConsent, \
    PreFlourishSubjectScreening, PreFlourishVisit

fake = Faker()

preflourishsubjectscreening = Recipe(
    PreFlourishSubjectScreening,
    has_child=YES,
)
childassent = Recipe(
    ChildAssent,
    subject_identifier=None,
    identity=seq('123476521'),
    confirm_identity=seq('123476521'),
    identity_type='OMANG',
    first_name=fake.first_name,
    last_name=fake.last_name,
    gender='M',
    hiv_testing=YES,
    remain_in_study=YES)

maternaldataset = Recipe(
    MaternalDataset,
)

preflourishconsent = Recipe(
    PreFlourishConsent,
    subject_identifier=None,
    consent_datetime=get_utcnow(),
    dob=get_utcnow() - relativedelta(years=25),
    first_name=fake.first_name,
    last_name=fake.last_name,
    initials='XX',
    gender='F',
    identity=seq('123425678'),
    confirm_identity=seq('123425678'),
    identity_type='OMANG',
    is_dob_estimated='-',
    version='1',
    consent_reviewed=YES,
    study_questions=YES,
    assessment_score=YES,
    consent_signature=YES,
    consent_copy=YES,
    child_consent=YES,
)

preflourishcaregiverchildconsent = Recipe(
    PreFlourishCaregiverChildConsent,
    first_name=fake.first_name,
    last_name=fake.last_name,
    subject_identifier='',
    gender='M',
    child_test=YES,
    child_dob=(get_utcnow() - relativedelta(years=3)).date(),
    child_remain_in_study=YES,
    child_preg_test=NOT_APPLICABLE,
    child_knows_status=YES,
    identity=seq('234513187'),
    identity_type='birth_cert',
    confirm_identity=seq('234513187')
)

preflourishchildassent = Recipe(
    PreFlourishChildAssent,
    subject_identifier=None,
    identity=seq('123476521'),
    confirm_identity=seq('123476521'),
    identity_type='OMANG',
    first_name=fake.first_name,
    last_name=fake.last_name,
    gender='M',
    hiv_testing=YES,
    remain_in_study=YES,
    preg_testing=YES,
    specimen_consent=YES,
    dob=(get_utcnow() - relativedelta(years=3)).date(),
    consent_datetime=get_utcnow(),
)

huupreenrollment = Recipe(
    HuuPreEnrollment,
)

preflourishvisit = Recipe(
    PreFlourishVisit,
    report_datetime=get_utcnow(),
    reason=SCHEDULED,
    study_status=ON_STUDY,
    survival_status=ALIVE,
    info_source=PARTICIPANT)

cyhuupreenrollment = Recipe(
    CyhuuPreEnrollment,
)

caregiverlocator = Recipe(
    CaregiverLocator,
    first_name=fake.first_name,
    last_name=fake.last_name,
    user_created='flourish')

pfchildhivrapidtestcounseling = Recipe(
    PFChildHIVRapidTestCounseling)

pfconsentversion = Recipe(
    PFConsentVersion)


cohortschedules = Recipe(
    CohortSchedules)

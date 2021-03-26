from dateutil.relativedelta import relativedelta
from edc_base.utils import get_utcnow
from edc_constants.constants import YES
from faker import Faker
from model_mommy.recipe import Recipe, seq

from .models import PreFlourishConsent, PreFlourishSubjectScreening

fake = Faker()

preflourishsubjectscreening = Recipe(
    PreFlourishSubjectScreening,
    age_in_years=25,
    has_omang=YES,
    has_child=YES,
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
)

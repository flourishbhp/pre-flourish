from dateutil.relativedelta import relativedelta
from django.test import TestCase
from edc_base import get_utcnow
from edc_constants.constants import FEMALE, YES
from edc_facility.import_holidays import import_holidays
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from model_mommy import mommy

from pre_flourish.models import OnScheduleChildPreFlourish, \
    PreFlourishChildDummySubjectConsent
from pre_flourish.models.appointment import Appointment


class TestPregnancyTestForm(TestCase):

    def setUp(self):
        import_holidays()

        self.caregiver_screening = mommy.make_recipe(
            'pre_flourish.preflourishsubjectscreening', )

        self.subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            screening_identifier=self.caregiver_screening.screening_identifier,
        )

        self.caregiver_child_consent = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=self.subject_consent,
            child_dob=get_utcnow() - relativedelta(years=15),
            gender=FEMALE
        )

        self.child_assent = mommy.make_recipe(
            'pre_flourish.preflourishchildassent',
            subject_identifier=self.caregiver_child_consent.subject_identifier,
            identity=self.caregiver_child_consent.identity,
            confirm_identity=self.caregiver_child_consent.identity,
            identity_type=self.caregiver_child_consent.identity_type,
            first_name=self.caregiver_child_consent.first_name,
            last_name=self.caregiver_child_consent.last_name,
            gender=self.caregiver_child_consent.gender,
            dob=self.caregiver_child_consent.child_dob,
        )

        self.dummy_consent = PreFlourishChildDummySubjectConsent.objects.get(
            subject_identifier=self.child_assent.subject_identifier)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.child_assent.subject_identifier,
            visit_code='1000')

    def test_func_hiv_test_required(self):
        self.assertEqual(OnScheduleChildPreFlourish.objects.filter(
            subject_identifier=self.caregiver_child_consent.subject_identifier).count(

        ), 1)

        pre_flourish_visit = mommy.make_recipe(
            'pre_flourish.preflourishvisit',
            appointment=self.appointment,
            report_datetime=self.dummy_consent.consent_datetime
        )

        self.assertEqual(CrfMetadata.objects.get(
            model='pre_flourish.pfinfanthivtesting',
            subject_identifier=pre_flourish_visit.subject_identifier,
            visit_code='1000').entry_status, NOT_REQUIRED)

        mommy.make_recipe(
            'pre_flourish.huupreenrollment',
            child_hiv_docs=YES,
            pre_flourish_visit=pre_flourish_visit,
            report_datetime=get_utcnow(),
            child_test_date=get_utcnow() - relativedelta(months=5))

        self.assertEqual(CrfMetadata.objects.get(
            model='pre_flourish.pfinfanthivtesting',
            subject_identifier=pre_flourish_visit.subject_identifier,
            visit_code='1000').entry_status, REQUIRED)

    def test_preg_test_required(self):
        self.assertEqual(OnScheduleChildPreFlourish.objects.filter(
            subject_identifier=self.caregiver_child_consent.subject_identifier).count(

        ), 1)

        visit = mommy.make_recipe(
            'pre_flourish.preflourishvisit',
            appointment=self.appointment,
            report_datetime=self.dummy_consent.consent_datetime
        )

        self.assertEqual(CrfMetadata.objects.get(
            model='pre_flourish.pfinfanthivtesting',
            subject_identifier=visit.subject_identifier,
            visit_code='1000').entry_status, NOT_REQUIRED)

        mommy.make_recipe(
            'pre_flourish.huupreenrollment',
            child_hiv_docs=YES,
            pre_flourish_visit=visit,
            report_datetime=get_utcnow(),
            child_test_date=get_utcnow() - relativedelta(months=5))

        self.assertEqual(CrfMetadata.objects.get(
            model='pre_flourish.pfinfanthivtesting',
            subject_identifier=visit.subject_identifier,
            visit_code='1000').entry_status, REQUIRED)

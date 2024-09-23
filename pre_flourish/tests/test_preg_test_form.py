from dateutil.relativedelta import relativedelta
from django.test import TestCase
from edc_base import get_utcnow
from edc_constants.constants import FEMALE
from edc_facility.import_holidays import import_holidays
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from model_mommy import mommy

from pre_flourish.models import OnScheduleChildPreFlourish
from pre_flourish.models.appointment import Appointment


class TestPregnancyTestForm(TestCase):

    def setUp(self):
        import_holidays()
        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        self.study_maternal_identifier = '89721'
        self.locator = mommy.make_recipe(
            'pre_flourish.caregiverlocator',
            study_maternal_identifier=self.study_maternal_identifier, )

        self.caregiver_screening = mommy.make_recipe(
            'pre_flourish.preflourishsubjectscreening',
            study_maternal_identifier=self.study_maternal_identifier)

        mommy.make_recipe(
            'pre_flourish.pfconsentversion',
            screening_identifier=self.caregiver_screening.screening_identifier,
            version='1',
            child_version='1'
        )

        self.subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            screening_identifier=self.caregiver_screening.screening_identifier,
            **self.options
        )

    def test_func_preg_test_required(self):
        """ Assert pregnancy testing CRF is required for all FEMALE
            participants 11 years or older.
        """
        caregiver_child_consent = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=self.subject_consent,
            child_dob=(get_utcnow() - relativedelta(years=15)).date(),
            gender=FEMALE,
            **self.options
        )

        child_assent = mommy.make_recipe(
            'pre_flourish.preflourishchildassent',
            subject_identifier=caregiver_child_consent.subject_identifier,
            identity=caregiver_child_consent.identity,
            confirm_identity=caregiver_child_consent.identity,
            identity_type=caregiver_child_consent.identity_type,
            first_name=caregiver_child_consent.first_name,
            last_name=caregiver_child_consent.last_name,
            gender=caregiver_child_consent.gender,
            dob=caregiver_child_consent.child_dob,
            **self.options
        )

        appointment = Appointment.objects.get(
            subject_identifier=child_assent.subject_identifier,
            visit_code='0200')

        self.assertEqual(OnScheduleChildPreFlourish.objects.filter(
            subject_identifier=caregiver_child_consent.subject_identifier).count(

        ), 1)

        pre_flourish_visit = mommy.make_recipe(
            'pre_flourish.preflourishvisit',
            appointment=appointment,
            report_datetime=child_assent.consent_datetime
        )

        self.assertEqual(CrfMetadata.objects.get(
            model='pre_flourish.pfchildpregtesting',
            subject_identifier=pre_flourish_visit.subject_identifier,
            visit_code='0200').entry_status, REQUIRED)

    def test_preg_test_not_required(self):
        """ Assert pregnancy testing CRF is not required for participant's
            less than 11 years of age.
        """
        caregiver_child_consent = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=self.subject_consent,
            child_dob=(get_utcnow() - relativedelta(years=10)).date(),
            gender=FEMALE,
            **self.options
        )

        child_assent = mommy.make_recipe(
            'pre_flourish.preflourishchildassent',
            subject_identifier=caregiver_child_consent.subject_identifier,
            identity=caregiver_child_consent.identity,
            confirm_identity=caregiver_child_consent.identity,
            identity_type=caregiver_child_consent.identity_type,
            first_name=caregiver_child_consent.first_name,
            last_name=caregiver_child_consent.last_name,
            gender=caregiver_child_consent.gender,
            dob=caregiver_child_consent.child_dob,
            **self.options
        )

        appointment = Appointment.objects.get(
            subject_identifier=child_assent.subject_identifier,
            visit_code='0200')

        self.assertEqual(OnScheduleChildPreFlourish.objects.filter(
            subject_identifier=caregiver_child_consent.subject_identifier).count(

        ), 1)

        visit = mommy.make_recipe(
            'pre_flourish.preflourishvisit',
            appointment=appointment,
            report_datetime=child_assent.consent_datetime
        )

        self.assertEqual(CrfMetadata.objects.get(
            model='pre_flourish.pfchildpregtesting',
            subject_identifier=visit.subject_identifier,
            visit_code='0200').entry_status, NOT_REQUIRED)

from dateutil.relativedelta import relativedelta
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import NO, YES
from edc_facility.import_holidays import import_holidays
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from model_mommy import mommy

from pre_flourish.models.appointment import Appointment


class TestHivRapidTestForm(TestCase):

    def setUp(self):
        import_holidays()
        self.subject_identifier = '12345678'
        self.study_maternal_identifier = '89721'

        self.locator = mommy.make_recipe(
            'pre_flourish.caregiverlocator',
            study_maternal_identifier=self.study_maternal_identifier, )

        self.caregiver_screening = mommy.make_recipe(
            'pre_flourish.preflourishsubjectscreening',
            study_maternal_identifier=self.study_maternal_identifier)

        self.subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            screening_identifier=self.caregiver_screening.screening_identifier,
        )

        self.pf_caregiver_child_consent = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=self.subject_consent,
            child_dob=get_utcnow() - relativedelta(years=11, months=5),
        )

        self.pf_child_assent = mommy.make_recipe(
            'pre_flourish.preflourishchildassent',
            subject_identifier=self.pf_caregiver_child_consent.subject_identifier,
            identity=self.pf_caregiver_child_consent.identity,
            confirm_identity=self.pf_caregiver_child_consent.identity,
            identity_type=self.pf_caregiver_child_consent.identity_type,
            first_name=self.pf_caregiver_child_consent.first_name,
            last_name=self.pf_caregiver_child_consent.last_name,
            gender=self.pf_caregiver_child_consent.gender,
            dob=self.pf_caregiver_child_consent.child_dob,
        )

        self.appointment = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='0200')

    def test_func_hiv_test_required(self):
        pre_flourish_visit = mommy.make_recipe(
            'pre_flourish.preflourishvisit',
            appointment=self.appointment,
            report_datetime=get_utcnow()
        )

        mommy.make_recipe(
            'pre_flourish.cyhuupreenrollment',
            pre_flourish_visit=pre_flourish_visit,
            hiv_docs=NO,
            report_datetime=get_utcnow(),
        )

        self.assertEqual(CrfMetadata.objects.get(
            model='pre_flourish.pfhivrapidtestcounseling',
            subject_identifier=pre_flourish_visit.subject_identifier,
            visit_code='0200').entry_status, REQUIRED)

    def test_func_hiv_test_not_required(self):
        pre_flourish_visit = mommy.make_recipe(
            'pre_flourish.preflourishvisit',
            appointment=self.appointment,
            report_datetime=get_utcnow()
        )

        mommy.make_recipe(
            'pre_flourish.cyhuupreenrollment',
            hiv_docs=YES,
            pre_flourish_visit=pre_flourish_visit,
            report_datetime=get_utcnow(),
        )

        self.assertEqual(CrfMetadata.objects.get(
            model='pre_flourish.pfhivrapidtestcounseling',
            subject_identifier=pre_flourish_visit.subject_identifier,
            visit_code='0200').entry_status, NOT_REQUIRED)

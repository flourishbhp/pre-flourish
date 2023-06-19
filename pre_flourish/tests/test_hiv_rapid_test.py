from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import FEMALE, YES, NO
from edc_facility.import_holidays import import_holidays
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from model_mommy import mommy

from pre_flourish.models import OnSchedulePreFlourish, \
    PreFlourishChildDummySubjectConsent
from pre_flourish.models.appointment import Appointment


class TestHivRapidTestForm(TestCase):

    def setUp(self):
        import_holidays()

        self.caregiver_screening = mommy.make_recipe(
            'pre_flourish.preflourishsubjectscreening', )

        self.subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            screening_identifier=self.caregiver_screening.screening_identifier,
        )

        self.appointment = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='1000')


    def test_func_hiv_test_required(self):
        pre_flourish_visit = mommy.make_recipe(
            'pre_flourish.preflourishvisit',
            appointment=self.appointment,
        )
        
        mommy.make_recipe(
            'pre_flourish.cyhuupreenrollment',
            pre_flourish_visit=pre_flourish_visit,
            hiv_docs=NO,
            report_datetime=datetime.now(),
            )


        self.assertEqual(CrfMetadata.objects.get(
            model='pre_flourish.pfhivrapidtestcounseling',
            subject_identifier=pre_flourish_visit.subject_identifier,
            visit_code='1000').entry_status, REQUIRED)

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
            visit_code='1000').entry_status, NOT_REQUIRED)


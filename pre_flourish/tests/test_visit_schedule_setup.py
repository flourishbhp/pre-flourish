from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_constants.constants import NO
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy
from ..models import OnSchedulePreFlourish


@tag('pre')
class TestVisitScheduleSetup(TestCase):

    def setUp(self):
        import_holidays()

        self.caregiver_screening = mommy.make_recipe(
            'pre_flourish.preflourishsubjectscreening',)

    def test_caregiver_onschedule_valid(self):
        subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            screening_identifier=self.caregiver_screening.screening_identifier)

        self.assertEqual(OnSchedulePreFlourish.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='pre_flourish_schedule1').count(), 1)

    def test_caregiver_onschedule_invalid(self):

        subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            subject_identifier='289415672',
            consent_reviewed=NO,
            screening_identifier=self.caregiver_screening.screening_identifier)

        self.assertEqual(OnSchedulePreFlourish.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='pre_flourish_schedule1').count(), 0)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 1)

from django.test import TestCase, tag
from ..models.appointment import Appointment
from edc_constants.constants import NO
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy
from ..models import OnSchedulePreFlourish, OnScheduleChildPreFlourish


@tag('pre')
class TestVisitScheduleSetup(TestCase):

    def setUp(self):
        import_holidays()

        self.caregiver_screening = mommy.make_recipe(
            'pre_flourish.preflourishsubjectscreening', )

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

    def test_child_onschedul(self):
        subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            screening_identifier=self.caregiver_screening.screening_identifier,
        )

        subject_consent.save()

        caregiver_child_consent = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=subject_consent,
        )
        caregiver_child_consent.save()

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
        )
        child_assent.save()

        self.assertEqual(OnScheduleChildPreFlourish.objects.filter(
            subject_identifier=caregiver_child_consent.subject_identifier).count(), 1)

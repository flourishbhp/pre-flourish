from django.test import TestCase, tag
from ..models.appointment import Appointment
from edc_constants.constants import NO, NEW, NEG, POS
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy
from ..models import OnSchedulePreFlourish, OnScheduleChildPreFlourish
from django.apps import apps as django_apps
from edc_action_item.site_action_items import site_action_items
from edc_base.utils import get_utcnow


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

    def test_child_onschedule(self):
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

    def test_child_off_study_required(self):
        subject_id = '11111111111111111'
        child_subject_id = '11111111111111111123'
        screening_identifier = '28941'

        subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            screening_identifier=self.caregiver_screening.screening_identifier)

        subject_consent.save()

        caregiver_child_consent = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=subject_consent,
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
        )

        appointment = Appointment.objects.get_or_create(
            subject_identifier=caregiver_child_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')

        pre_flourish_visit = mommy.make_recipe(
            'pre_flourish.preflourishvisit',
            appointment=appointment,
        )
        mommy.make_recipe(
            'pre_flourish.huupreenrollment',
            child_hiv_result=POS,
            pre_flourish_visit=pre_flourish_visit, )

        child_off_study_cls = django_apps.get_model(
            'pre_flourish.preflourishchildoffstudy'
        )

        action_cls = site_action_items.get(child_off_study_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item_obj = action_item_model_cls.objects.get(
                subject_identifier=caregiver_child_consent.subject_identifier,
                action_type__name=child_off_study_cls.action_name,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            self.fail('Action Item to created')
        else:
            self.assertNotIsInstance(obj=action_item_obj, cls=action_item_model_cls)

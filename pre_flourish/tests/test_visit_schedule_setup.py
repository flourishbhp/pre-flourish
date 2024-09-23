from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from ..models.appointment import Appointment
from edc_constants.constants import FEMALE, NO, NEW, NEG, POS
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

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        self.caregiver_screening = mommy.make_recipe(
            'pre_flourish.preflourishsubjectscreening', )

        mommy.make_recipe(
            'pre_flourish.pfconsentversion',
            screening_identifier=self.caregiver_screening.screening_identifier,
            version='1',
            child_version='1'
        )

    @tag('ssaa')
    def test_caregiver_onschedule_invalid(self):
        subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            screening_identifier=self.caregiver_screening.screening_identifier,
            **self.options)

        caregiver_child_consent = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=subject_consent,
            child_dob=(get_utcnow() - relativedelta(years=15)).date(),
            gender=FEMALE,
            **self.options
        )

        mommy.make_recipe(
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

        self.assertEqual(OnSchedulePreFlourish.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='pre_flourish_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 0)

    def test_child_onschedule(self):
        subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            screening_identifier=self.caregiver_screening.screening_identifier,
            **self.options
        )

        caregiver_child_consent = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=subject_consent,
            **self.options
        )

        mommy.make_recipe(
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

        self.assertEqual(OnScheduleChildPreFlourish.objects.filter(
            subject_identifier=caregiver_child_consent.subject_identifier).count(), 1)

    def test_child_off_study_required(self):

        subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            screening_identifier=self.caregiver_screening.screening_identifier,
            **self.options)

        caregiver_child_consent = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=subject_consent,
            child_dob=(get_utcnow() - relativedelta(years=15)).date(),
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

        pre_flourish_visit = mommy.make_recipe(
            'pre_flourish.preflourishvisit',
            appointment=appointment,
            report_datetime=get_utcnow()
        )

        mommy.make_recipe(
            'pre_flourish.huupreenrollment',
            child_hiv_result=POS,
            report_datetime=get_utcnow(),
            pre_flourish_visit=pre_flourish_visit, )

        child_off_study_cls = django_apps.get_model(
            'pre_flourish.preflourishchildoffstudy'
        )

        action_cls = site_action_items.get(child_off_study_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item_model_cls.objects.get(
                subject_identifier=caregiver_child_consent.subject_identifier,
                action_type__name=child_off_study_cls.action_name,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            self.fail('Action Item not created')

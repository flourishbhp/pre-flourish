from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base import get_utcnow
from edc_constants.constants import NEG, NOT_APPLICABLE, YES, NO
from edc_facility.import_holidays import import_holidays
from edc_registration.models import RegisteredSubject
from edc_visit_schedule.models import SubjectScheduleHistory
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from flourish_caregiver.models import MaternalDataset
from flourish_child.models import ChildDataset
from pre_flourish.models import PreFlourishRegisteredSubject
from pre_flourish.models.appointment import Appointment


def create_caregiver_cohort_schedules():
    cohorts = ['a', 'b', 'c']
    for cohort in cohorts:
        _count = 1
        while _count <= 3:
            mommy.make_recipe(
                'flourish_caregiver.cohortschedules',
                schedule_name=f'{cohort}_fu{_count}_schedule1',
                schedule_type='followup',
                cohort_name=f'cohort_{cohort}',
                onschedule_model=f'flourish_caregiver.onschedulecohort{cohort}fu',
                child_count=_count
            )
            _count += 1


def create_child_cohort_schedules():
    cohorts = ['a', 'b', 'c']
    for cohort in cohorts:
        mommy.make_recipe(
            'flourish_caregiver.cohortschedules',
            schedule_name=f'child_{cohort}_fu_schedule1',
            schedule_type='followup',
            cohort_name=f'cohort_{cohort}',
            onschedule_model=f'flourish_child.onschedulechildcohort{cohort}fu',
            child_count=None
        )


@tag('enrol')
class TestFlourishEnrolment(TestCase):
    databases = '__all__'

    def setUp(self):
        import_holidays()
        self.subject_identifier = '12345678'
        self.study_maternal_identifier = '89721'
        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        create_caregiver_cohort_schedules()

        create_child_cohort_schedules()

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

        self.pre_flourish_subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            screening_identifier=self.caregiver_screening.screening_identifier,
            **self.options)

        self.pf_caregiver_child_consent = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=self.pre_flourish_subject_consent,
            child_dob=(get_utcnow() - relativedelta(years=11, months=5)).date(),
            **self.options
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
            **self.options,
        )

    @tag('sdes')
    def test_creates_caregiver_registered_subject(self):
        self.assertEqual(PreFlourishRegisteredSubject.objects.filter(
            subject_identifier=self.pre_flourish_subject_consent.subject_identifier
        ).count(), 1)
        self.assertEqual(RegisteredSubject.objects.filter(
            subject_identifier=self.pre_flourish_subject_consent.subject_identifier
        ).count(), 0)

    def test_create_child_registered_subject(self):
        self.assertEqual(PreFlourishRegisteredSubject.objects.filter(
            subject_identifier=self.pf_caregiver_child_consent.subject_identifier
        ).count(), 1)
        self.assertEqual(RegisteredSubject.objects.filter(
            subject_identifier=self.pf_caregiver_child_consent.subject_identifier
        ).count(), 0)

    @tag('dset')
    def test_create_dataset(self):
        self.assertEqual(MaternalDataset.objects.filter(
            study_maternal_identifier=self.study_maternal_identifier).count(), 0)
        self.assertEqual(ChildDataset.objects.filter(
            study_child_identifier=self.pf_child_assent.subject_identifier).count(), 0)

        visit = mommy.make_recipe(
            'pre_flourish.preflourishvisit',
            appointment=Appointment.objects.get(
                visit_code='0200',
                subject_identifier=self.pf_caregiver_child_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'pre_flourish.huupreenrollment',
            pre_flourish_visit=visit,
            child_test_date=get_utcnow().date(),
            child_hiv_result=NEG,
            report_datetime=get_utcnow(),
            child_weight_kg=34.0,
            child_height=141.0, )

        self.assertEqual(MaternalDataset.objects.filter(
            study_maternal_identifier=self.study_maternal_identifier).count(), 1)

        self.assertEqual(ChildDataset.objects.filter(
            study_child_identifier=self.pf_child_assent.subject_identifier).count(), 1)

    def test_rapid_hiv_create_maternal_dataset(self):
        visit = mommy.make_recipe(
            'pre_flourish.preflourishvisit',
            appointment=Appointment.objects.get(
                visit_code='0200',
                subject_identifier=self.pf_caregiver_child_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        hiv_test_data = {
            'report_datetime': get_utcnow(),
            'rapid_test_done': YES,
            'result_date': get_utcnow().date(),
            'result': NEG,
            'comments': None, }

        mommy.make_recipe(
            'pre_flourish.pfchildhivrapidtestcounseling',
            pre_flourish_visit=visit,
            **hiv_test_data)

        self.assertEqual(MaternalDataset.objects.filter(
            study_maternal_identifier=self.study_maternal_identifier).count(), 1)

        self.assertEqual(ChildDataset.objects.filter(
            study_child_identifier=self.pf_child_assent.subject_identifier).count(), 1)

    @tag('flo-enrol')
    def test_enrolment(self):
        visit = mommy.make_recipe(
            'pre_flourish.preflourishvisit',
            appointment=Appointment.objects.get(
                visit_code='0200',
                subject_identifier=self.pf_caregiver_child_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'pre_flourish.huupreenrollment',
            pre_flourish_visit=visit,
            child_test_date=get_utcnow().date(),
            child_hiv_result=NEG,
            report_datetime=get_utcnow(),
            child_weight_kg=34.0,
            child_height=141.0, )

        prior_screening = mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=self.pre_flourish_subject_consent.screening_identifier,
            study_maternal_identifier=self.study_maternal_identifier)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=prior_screening.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            biological_caregiver=YES,
            **self.options)

        child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=self.pf_child_assent.subject_identifier,
            child_dob=self.pf_child_assent.dob,
            **self.options)

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=subject_consent.subject_identifier)

        # Check caregiver is not put on enrolment schedule.
        enrol_schedule = SubjectScheduleHistory.objects.filter(
            schedule_name='c_enrol1_schedule1',
            subject_identifier=subject_consent.subject_identifier)
        self.assertEquals(0, enrol_schedule.count())

        # Check caregiver enroled on FU schedule.
        fu_schedule = SubjectScheduleHistory.objects.filter(
            schedule_name='c_fu1_schedule1',
            subject_identifier=subject_consent.subject_identifier)
        self.assertEquals(1, fu_schedule.count())

        # Check child enroled on FU schedule
        child_enrol_schedule = SubjectScheduleHistory.objects.filter(
            schedule_name='child_c_fu_schedule1',
            subject_identifier=child_consent.subject_identifier)
        self.assertEquals(1, child_enrol_schedule.count())

    def test_registered_subject(self):
        registered_subject = PreFlourishRegisteredSubject.objects.get(
            identity=self.pre_flourish_subject_consent.identity)

        self.assertEqual(registered_subject.subject_identifier,
                         self.pre_flourish_subject_consent.subject_identifier)
        prior_screening = mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            study_maternal_identifier=self.study_maternal_identifier)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=prior_screening.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            biological_caregiver=YES,
            **self.options)

        registered_subject = RegisteredSubject.objects.get(
            identity=subject_consent.identity)

        self.assertEqual(registered_subject.subject_identifier,
                         subject_consent.subject_identifier)

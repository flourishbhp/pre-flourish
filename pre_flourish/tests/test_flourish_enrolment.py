from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base import get_utcnow
from edc_constants.constants import NEG, NOT_APPLICABLE, YES
from edc_facility.import_holidays import import_holidays
from edc_registration.models import RegisteredSubject
from edc_visit_schedule.models import SubjectScheduleHistory
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from flourish_caregiver.models import MaternalDataset
from flourish_child.models import ChildDataset
from pre_flourish.models import PreFlourishRegisteredSubject
from pre_flourish.models.appointment import Appointment


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

        self.locator = mommy.make_recipe(
            'pre_flourish.caregiverlocator',
            study_maternal_identifier=self.study_maternal_identifier, )

        self.caregiver_screening = mommy.make_recipe(
            'pre_flourish.preflourishsubjectscreening',
            study_maternal_identifier=self.study_maternal_identifier)

        self.pre_flourish_subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            screening_identifier=self.caregiver_screening.screening_identifier)

        self.pre_flourish_subject_consent.save()

        self.pf_caregiver_child_consent = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=self.pre_flourish_subject_consent,
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

    @tag('sdes')
    def test_creates_caregiver_registered_subject(self):
        caregiver_screening = mommy.make_recipe(
            'pre_flourish.preflourishsubjectscreening', )

        pre_flourish_subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            screening_identifier=caregiver_screening.screening_identifier)

        self.assertEqual(PreFlourishRegisteredSubject.objects.filter(
            subject_identifier=pre_flourish_subject_consent.subject_identifier
        ).count(), 1)
        self.assertEqual(RegisteredSubject.objects.filter(
            subject_identifier=pre_flourish_subject_consent.subject_identifier
        ).count(), 0)

    def test_create_child_registered_subject(self):
        caregiver_screening = mommy.make_recipe(
            'pre_flourish.preflourishsubjectscreening', )

        pre_flourish_subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            screening_identifier=caregiver_screening.screening_identifier)

        pre_flourish_subject_consent.save()

        pf_caregiver_child_consent = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=pre_flourish_subject_consent,
        )
        mommy.make_recipe(
            'pre_flourish.preflourishchildassent',
            subject_identifier=pf_caregiver_child_consent.subject_identifier,
            identity=pf_caregiver_child_consent.identity,
            confirm_identity=pf_caregiver_child_consent.identity,
            identity_type=pf_caregiver_child_consent.identity_type,
            first_name=pf_caregiver_child_consent.first_name,
            last_name=pf_caregiver_child_consent.last_name,
            gender=pf_caregiver_child_consent.gender,
            dob=pf_caregiver_child_consent.child_dob,
        )
        self.assertEqual(PreFlourishRegisteredSubject.objects.filter(
            subject_identifier=pf_caregiver_child_consent.subject_identifier
        ).count(), 1)
        self.assertEqual(RegisteredSubject.objects.filter(
            subject_identifier=pf_caregiver_child_consent.subject_identifier
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
            child_test_date=get_utcnow(),
            child_hiv_result=NEG,
            report_datetime=get_utcnow(), )

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
            child_test_date=get_utcnow(),
            child_hiv_result=NEG,
            report_datetime=get_utcnow(), )

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

        mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=self.pf_child_assent.subject_identifier,
            child_dob=self.pf_child_assent.dob, )

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=subject_consent.subject_identifier)

        schedules = SubjectScheduleHistory.objects.filter(schedule_name__startswith='c_',
                                                          subject_identifier=subject_consent.subject_identifier)
        self.assertNotEquals(0, schedules.count())

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

from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import TestCase, tag
from edc_base import get_utcnow
from edc_constants.constants import MALE, NOT_APPLICABLE
from edc_facility.import_holidays import import_holidays
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from pre_flourish.helper_classes.heu_huu_matching_helper import HEUHUUMatchingHelper
from pre_flourish.models import HeuHuuMatch, \
    PreFlourishChildDummySubjectConsent
from pre_flourish.models.appointment import Appointment
from pre_flourish.models.caregiver import OnScheduleChildPreFlourish
from flourish_child.models import Appointment as ChildAppointment


@tag('heu_huu')
class TestHEUHUUMatch(TestCase):

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '2'}

        maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=15, months=2),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': '12345',
            'protocol': 'Mashi',
            'preg_pi': 1}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': '12345',
            'study_child_identifier': '1234',
            'infant_sex':MALE
        }

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=15, months=2),
            **self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **maternal_dataset_options)

        self.flourish_consent_version = mommy.make_recipe(
            'flourish_caregiver.flourishconsentversion',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            version='2',
            child_version='2')

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            subject_identifier=maternal_dataset_obj.subject_identifier, )

        self.subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            **self.options)

        screening_cls = django_apps.get_model(
            'flourish_caregiver.screeningpriorbhpparticipants')

        screening_obj = screening_cls.objects.get(
            screening_identifier=self.subject_consent.screening_identifier)

        screening_obj.subject_identifier = self.subject_consent.subject_identifier

        screening_obj.save()

        caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=self.subject_consent,
            study_child_identifier=self.child_dataset_options.get(
                'study_child_identifier'),
            identity='126513789',
            confirm_identity='126513789',
            child_dob=(get_utcnow() - relativedelta(years=15, months=2)).date(),
            gender=MALE)
        caregiver_child_consent_obj.version = '2'
        caregiver_child_consent_obj.save()

        self.child_subject_identifier = caregiver_child_consent_obj.subject_identifier

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=self.subject_consent.subject_identifier)

        flourish_child_assent = mommy.make_recipe(
            'flourish_child.childassent',
            subject_identifier=caregiver_child_consent_obj.subject_identifier,
            dob=caregiver_child_consent_obj.child_dob,
            gender='M',
            identity=caregiver_child_consent_obj.identity,
            confirm_identity=caregiver_child_consent_obj.identity,
            version=self.subject_consent.version)

        flourish_child_visit = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=ChildAppointment.objects.get(
                visit_code='2000',
                subject_identifier=flourish_child_assent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.childclinicalmeasurements',
            child_visit=flourish_child_visit,
            child_weight_kg=20,
            child_height=130
        )

    def test_heu_huu_match(self):
        """Assert that the child is matched to the HEU participant."""
        heu_huu_matching_helper = HEUHUUMatchingHelper(dob=None, child_weight_kg=None,
                                                       child_height_cm=None,
                                                       subject_identifier=None)

        heu_subject = {
            'subject_identifier': '12345',
            'age': 10,
            'bmi': 17
        }

        huu_subject_2 = {
            'subject_identifier': '4567',
            'age': 13,
            'bmi': 16
        }

        self.assertTrue(
            heu_huu_matching_helper.have_matching_age_bmi(subject_1=heu_subject,
                                                          subject_2=huu_subject_2))

    def test_heu_huu_not_match_age(self):
        """Assert that the child is matched to the HEU participant."""
        heu_huu_matching_helper = HEUHUUMatchingHelper(dob=None, child_weight_kg=None,
                                                       child_height_cm=None,
                                                       subject_identifier=None)

        heu_subject = {
            'subject_identifier': '12345',
            'age': 14,
            'bmi': 17
        }

        huu_subject_2 = {
            'subject_identifier': '4567',
            'age': 13,
            'bmi': 20
        }

        self.assertNotEquals(
            heu_huu_matching_helper.have_matching_age_bmi(subject_1=heu_subject,
                                                          subject_2=huu_subject_2), True)

    def test_heu_huu_not_match_age_not_in_bin(self):
        """Assert that the child is matched to the HEU participant."""
        heu_huu_matching_helper = HEUHUUMatchingHelper(dob=None, child_weight_kg=None,
                                                       child_height_cm=None,
                                                       subject_identifier=None)

        heu_subject = {
            'subject_identifier': '12345',
            'age': 9,
            'bmi': 17
        }

        huu_subject_2 = {
            'subject_identifier': '4567',
            'age': 13,
            'bmi': 20
        }

        self.assertNotEquals(
            heu_huu_matching_helper.have_matching_age_bmi(subject_1=heu_subject,
                                                          subject_2=huu_subject_2), True)

    def test_heu_huu_not_match_bmi(self):
        """Assert that the child is matched to the HEU participant."""
        heu_huu_matching_helper = HEUHUUMatchingHelper(
            dob=None, child_weight_kg=None, child_height_cm=None, subject_identifier=None
        )

        heu_subject = {
            'subject_identifier': '12345',
            'age': 10,
            'bmi': 17
        }

        huu_subject_2 = {
            'subject_identifier': '4567',
            'age': 13,
            'bmi': 25
        }

        self.assertNotEquals(
            heu_huu_matching_helper.have_matching_age_bmi(subject_1=heu_subject,
                                                          subject_2=huu_subject_2), True)

    def test_heu_huu_not_match_bmi_none(self):
        """Assert that the child is matched to the HEU participant."""
        heu_huu_matching_helper = HEUHUUMatchingHelper(dob=None, child_weight_kg=None,
                                                       child_height_cm=None,
                                                       subject_identifier=None)

        heu_subject = {
            'subject_identifier': '12345',
            'age': 10,
            'bmi': 17
        }

        huu_subject_2 = {
            'subject_identifier': '4567',
            'age': 13,
            'bmi': None
        }

        self.assertNotEquals(
            heu_huu_matching_helper.have_matching_age_bmi(subject_1=heu_subject,
                                                          subject_2=huu_subject_2), True)

    @tag('huu')
    def test_huu_participant_match(self):
        self.caregiver_screening = mommy.make_recipe(
            'pre_flourish.preflourishsubjectscreening', )

        subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            screening_identifier=self.caregiver_screening.screening_identifier,
            **self.options)

        caregiver_child_consent = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=subject_consent,
        )

        pre_flourish_child_assent_obj = mommy.make_recipe(
            'pre_flourish.preflourishchildassent',
            subject_identifier=caregiver_child_consent.subject_identifier,
            identity=caregiver_child_consent.identity,
            confirm_identity=caregiver_child_consent.identity,
            identity_type=caregiver_child_consent.identity_type,
            first_name=caregiver_child_consent.first_name,
            last_name=caregiver_child_consent.last_name,
            gender=caregiver_child_consent.gender,
            dob=caregiver_child_consent.child_dob, )

        self.assertEqual(PreFlourishChildDummySubjectConsent.objects.filter(
            subject_identifier=pre_flourish_child_assent_obj.subject_identifier).count(),
                         1)

        self.assertEqual(OnScheduleChildPreFlourish.objects.filter(
            subject_identifier=pre_flourish_child_assent_obj.subject_identifier,
            schedule_name='pf_child_schedule1').count(), 1)

        child_visit = mommy.make_recipe(
            'pre_flourish.preflourishvisit',
            appointment=Appointment.objects.get(
                visit_code='1000',
                subject_identifier=pre_flourish_child_assent_obj.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(CrfMetadata.objects.get(
            model='pre_flourish.huupreenrollment',
            subject_identifier=pre_flourish_child_assent_obj.subject_identifier,
            visit_code='1000').entry_status, REQUIRED)

        mommy.make_recipe(
            'pre_flourish.huupreenrollment',
            pre_flourish_visit=child_visit,
            height=130,
            weight=20)

        self.assertEqual(HeuHuuMatch.objects.filter(
            huu_prt=pre_flourish_child_assent_obj.subject_identifier).count(), 1)

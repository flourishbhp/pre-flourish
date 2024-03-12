from dateutil.relativedelta import relativedelta
from django.test import tag, TestCase
from edc_base import get_utcnow
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from pre_flourish.models import PFConsentVersion
from pre_flourish.models.appointment import Appointment


@tag('reconsent')
class Reconsent(TestCase):
    def setUp(self):
        import_holidays()
        self.subject_identifier = '12345678'
        self.study_maternal_identifier = '89721'
        self.options = {
            'version': '1'}

        self.locator = mommy.make_recipe(
            'pre_flourish.caregiverlocator',
            study_maternal_identifier=self.study_maternal_identifier, )

        self.caregiver_screening = mommy.make_recipe(
            'pre_flourish.preflourishsubjectscreening',
            study_maternal_identifier=self.study_maternal_identifier)

        self.pre_flourish_subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            screening_identifier=self.caregiver_screening.screening_identifier,
            version='1')

        self.pre_flourish_subject_consent.save()

        self.pf_caregiver_child_consent = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=self.pre_flourish_subject_consent,
            child_dob=get_utcnow() - relativedelta(years=11, months=5),
            version='1'
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

        Appointment.objects.get(
            visit_code='0200',
            subject_identifier=self.pf_caregiver_child_consent.subject_identifier)

    def test_reconsent(self):
        consent_version_obj = PFConsentVersion.objects.get(
            screening_identifier=self.caregiver_screening.screening_identifier)
        consent_version_obj.version = '4'
        consent_version_obj.child_version = '4'
        consent_version_obj.save()
        version_4 = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            subject_identifier=self.pre_flourish_subject_consent.subject_identifier,
            screening_identifier=self.pre_flourish_subject_consent.screening_identifier,
            version='4'
        )

        child_version_4 = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=version_4,
            child_dob=get_utcnow() - relativedelta(years=11, months=5),
            version='4'
        )

        self.assertEqual(version_4.version, '4')
        self.assertEqual(child_version_4.version, '4')


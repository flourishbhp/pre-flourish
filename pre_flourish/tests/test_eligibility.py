from django.test import TestCase, tag
from django.conf import settings
from django.shortcuts import reverse
from edc_constants.constants import NO, YES

from pre_flourish.constants import MIN_AGE_OF_CONSENT
from pre_flourish.models.caregiver.eligibility import Eligibility


@tag('eligible')
class TestEligibility(TestCase):
    def test_participant_age_ineligible(self):
        eligibility = Eligibility(
            willing_consent=YES,
            willing_assent=YES,
            study_interest=YES,
            caregiver_age=16,
            caregiver_omang=YES,
            has_child=YES,
            remain_in_study=YES)

        self.assertFalse(eligibility.is_eligible)
        self.assertIn('Mother is under {}'.format(MIN_AGE_OF_CONSENT),
                      eligibility.error_message)

    def test_participant_no_omang_ineligible(self):
        eligibility = Eligibility(
            willing_consent=YES,
            willing_assent=YES,
            study_interest=YES,
            caregiver_age=20,
            caregiver_omang=NO,
            has_child=YES,
            remain_in_study=YES)

        self.assertFalse(eligibility.is_eligible)
        self.assertIn('Not a citizen', eligibility.error_message)

    def test_participant_study_interest_ineligible(self):
        eligibility = Eligibility(
            willing_consent=YES,
            willing_assent=YES,
            study_interest=NO,
            caregiver_age=20,
            caregiver_omang=YES,
            has_child=YES,
            remain_in_study=YES)

        self.assertFalse(eligibility.is_eligible)
        self.assertIn('Not interested in study', eligibility.error_message)

    def test_participant_willing_to_consent_ineligible(self):
        eligibility = Eligibility(
            willing_consent=NO,
            willing_assent=YES,
            study_interest=YES,
            caregiver_age=20,
            caregiver_omang=YES,
            has_child=YES,
            remain_in_study=YES)

        self.assertFalse(eligibility.is_eligible)
        self.assertIn('Not willing to consent', eligibility.error_message)

    def test_participant_willing_to_assent_ineligible(self):
        eligibility = Eligibility(
            willing_consent=YES,
            willing_assent=NO,
            study_interest=YES,
            caregiver_age=20,
            caregiver_omang=YES,
            has_child=YES,
            remain_in_study=YES)

        self.assertFalse(eligibility.is_eligible)
        self.assertIn('Child is not willing to assent', eligibility.error_message)

    def test_participant_has_child_ineligible(self):
        eligibility = Eligibility(
            willing_consent=YES,
            willing_assent=YES,
            study_interest=YES,
            caregiver_age=20,
            caregiver_omang=YES,
            has_child=NO,
            remain_in_study=YES)

        self.assertFalse(eligibility.is_eligible)
        self.assertIn('Does not have a child > 10 years', eligibility.error_message)

    def test_participant_remain_in_study_ineligible(self):
        eligibility = Eligibility(
            willing_consent=YES,
            willing_assent=YES,
            study_interest=YES,
            caregiver_age=20,
            caregiver_omang=YES,
            has_child=YES,
            remain_in_study=NO)

        self.assertFalse(eligibility.is_eligible)
        self.assertIn('Participant is not willing to remain in study area until 2025.',
                      eligibility.error_message)

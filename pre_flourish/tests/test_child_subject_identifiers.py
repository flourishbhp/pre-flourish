import re
from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from model_mommy import mommy

from edc_constants.constants import NO, YES, FEMALE
from edc_facility.import_holidays import import_holidays

subject_identifier = '[B|C]142\-[0-9\-]+'


@tag('sidx')
class TestSubjectIdentifier(TestCase):

    def setUp(self):
        import_holidays()
        screening_options = {
            'valid_identification': YES,
            'biological_mother': YES,
            'biological_mother_in_bcpp': YES,
            'caregiver_age': 28,
            'remain_in_study': YES,
            'willing_consent': YES,
            'has_child': YES,
            'willing_assent': YES,
            'study_interest': YES, }

        self.subject_screening = mommy.make_recipe(
            'pre_flourish.preflourishsubjectscreening',
            **screening_options)

        self.consent_options = {
            'screening_identifier': self.subject_screening.screening_identifier,
            'future_contact': YES,
            'child_consent': YES,
            'biological_caregiver': YES,
            'consent_datetime': get_utcnow,
            'consent_reviewed': YES,
            'study_questions': YES,
            'assessment_score': YES,
            'consent_signature': YES,
            'consent_copy': YES, }

        self.child_consent_options = {
            'gender': FEMALE,
            'child_dob': (get_utcnow() - relativedelta(years=12)).date(),
            'child_preg_test': YES,
            'future_studies_contact': YES}

        self.subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            **self.consent_options)

    def test_subject_identifier_bio_mother(self):
        """ Test consent allocates subject identifier starting with a
            B for a biological mother enrolling with the child
        """
        self.assertTrue(
            self.subject_consent.subject_identifier.startswith('B'))

    def test_subject_identifier_caregiver(self):
        self.consent_options.update({'biological_caregiver': NO})
        subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            **self.consent_options)

        self.assertTrue(subject_consent.subject_identifier.startswith('C'))

    def test_child_identifier_sequence_siblings(self):
        """ Test child subject identifier postfix assigned correctly for siblings
        """
        child_consent1 = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=self.subject_consent,
            **self.child_consent_options)

        self.child_consent_options.update(
            {'dob': (get_utcnow() - relativedelta(years=10)).date(), })

        child_consent2 = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=self.subject_consent,
            **self.child_consent_options)

        self.assertTrue(
            re.match(child_consent1.subject_identifier,
                     self.subject_consent.subject_identifier + '-10'))

        self.assertTrue(
            re.match(child_consent2.subject_identifier,
                     self.subject_consent.subject_identifier + '-60'))

    def test_child_identifier_sequence_twins(self):
        """ Test child subject identifier postfix assigned correctly for twins
        """
        self.consent_options.update({'multiple_births': 'twins'})

        subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            **self.consent_options)

        self.child_consent_options.update({'twin_triplet': True})

        child_consent1 = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=subject_consent,
            **self.child_consent_options)

        child_consent2 = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=subject_consent,
            **self.child_consent_options)

        self.assertTrue(
            re.match(child_consent1.subject_identifier,
                     subject_consent.subject_identifier + '-25'))

        self.assertTrue(
            re.match(child_consent2.subject_identifier,
                     subject_consent.subject_identifier + '-35'))

    def test_child_identifier_sequence_triplets(self):
        """ Test child subject identifier postfix assigned correctly for triplets
        """
        self.consent_options.update({'multiple_births': 'triplets'})

        subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            **self.consent_options)

        self.child_consent_options.update({'twin_triplet': True})

        child_consent1 = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=subject_consent,
            **self.child_consent_options)

        child_consent2 = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=subject_consent,
            **self.child_consent_options)

        child_consent3 = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=subject_consent,
            **self.child_consent_options)

        self.assertTrue(
            re.match(child_consent1.subject_identifier,
                     subject_consent.subject_identifier + '-36'))

        self.assertTrue(
            re.match(child_consent2.subject_identifier,
                     subject_consent.subject_identifier + '-46'))

        self.assertTrue(
            re.match(child_consent3.subject_identifier,
                     subject_consent.subject_identifier + '-56'))

    def test_child_identifier_seq_twins_siblings(self):
        """ Test child subject identifier postfix assigned correctly for twins
            and sibling enrolled.
        """
        self.consent_options.update({'multiple_births': 'twins'})

        subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            **self.consent_options)

        self.child_consent_options.update({'twin_triplet': True})

        child_consent1 = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=subject_consent,
            **self.child_consent_options)

        child_consent2 = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=subject_consent,
            **self.child_consent_options)

        self.child_consent_options.update({'twin_triplet': False})
        child_consent3 = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=subject_consent,
            **self.child_consent_options)

        self.assertTrue(
            re.match(child_consent1.subject_identifier,
                     subject_consent.subject_identifier + '-25'))

        self.assertTrue(
            re.match(child_consent2.subject_identifier,
                     subject_consent.subject_identifier + '-35'))

        self.assertTrue(
            re.match(child_consent3.subject_identifier,
                     subject_consent.subject_identifier + '-70'))

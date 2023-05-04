from edc_constants.constants import NO

from ...constants import (MAX_AGE_OF_CONSENT, MIN_AGE_OF_CONSENT)


class Eligibility:

    def __init__(self, willing_consent=None, has_child=None, caregiver_age=None,
                 caregiver_omang=None, willing_assent=None, study_interest=None,
                 remain_in_study=None, **kwargs):
        """checks if mother is eligible otherwise'
        ' error message is the reason for'
        ' eligibility test failed."""
        self.caregiver_age = caregiver_omang
        self.error_message = []
        if willing_consent == NO:
            self.error_message.append('Not willing to consent')

        if caregiver_age < MIN_AGE_OF_CONSENT:
            self.error_message.append(
                'Mother is under {}'.format(MIN_AGE_OF_CONSENT))

        if caregiver_age > MAX_AGE_OF_CONSENT:
            self.error_message.append(
                'Mother is too old (>{})'.format(MAX_AGE_OF_CONSENT))

        if caregiver_omang == NO:
            self.error_message.append('Not a citizen')

        if has_child == NO:
            self.error_message.append('Does not have a child > 10 years')

        if willing_assent == NO:
            self.error_message.append('Child is not willing to assent')

        if study_interest == NO:
            self.error_message.append('Not interested in study')

        if remain_in_study == NO:
            self.error_message.append(
                'Participant is not willing to remain in study area until 2025.')

        self.is_eligible = False if self.error_message else True

    def __str__(self):
        return "Screened, age ({})".format(self.caregiver_age)


class ConsentEligibility:

    def __init__(self, hiv_testing=None, breastfeed_intent=None,
                 consent_reviewed=None, study_questions=None, assessment_score=None,
                 consent_signature=None, consent_copy=None, child_consent=None):
        self.error_message = []
        self.hiv_testing = hiv_testing
        self.breastfeed_intent = breastfeed_intent
        self.consent_reviewed = consent_reviewed
        self.study_questions = study_questions
        self.assessment_score = assessment_score
        self.consent_signature = consent_signature
        self.consent_copy = consent_copy
        self.child_consent = child_consent
        if self.hiv_testing == NO:
            self.error_message.append(
                'Participant is not willing to undergo HIV testing and counseling.')
        if self.breastfeed_intent == NO:
            self.error_message.append(
                'Participant does not intend on breastfeeding.')
        if self.consent_reviewed == NO:
            self.error_message.append(
                'Consent was not reviewed with the participant.')
        if self.study_questions == NO:
            self.error_message.append(
                'Did not answer all questions the participant had about the study.')
        if self.assessment_score == NO:
            self.error_message.append(
                'Participant did not demonstrate understanding of the study.')
        if self.consent_signature == NO:
            self.error_message.append(
                'Participant did not sign the consent form.')
        if self.consent_copy == NO:
            self.error_message.append(
                'Participant was not provided with a copy of their informed consent.')
        if self.child_consent == NO:
            self.error_message.append(
                'Participant is not willing to consent for their child\'s participation.')
        self.is_eligible = False if self.error_message else True

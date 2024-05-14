from django.test import TestCase, tag
from django.core.exceptions import ValidationError
from edc_constants.constants import FEMALE, NOT_APPLICABLE, YES
from pre_flourish.form_validators.pre_flourish_child_assent_validator import PreFlourishChildAssentFormValidator
from edc_base import get_utcnow
from dateutil.relativedelta import relativedelta
from model_mommy import mommy
from edc_facility.import_holidays import import_holidays


@tag('preg')
class TestPreFlourishChildAssentValidatorForm (TestCase):
    def setUp(self):

        import_holidays()
        self.caregiver_screening = mommy.make_recipe(
            'pre_flourish.preflourishsubjectscreening', )

        self.subject_consent = mommy.make_recipe(
            'pre_flourish.preflourishconsent',
            screening_identifier=self.caregiver_screening.screening_identifier,
        )

        self.caregiver_child_consent = mommy.make_recipe(
            'pre_flourish.preflourishcaregiverchildconsent',
            subject_consent=self.subject_consent,
            child_dob=get_utcnow() - relativedelta(years=14),
            gender=FEMALE,
        )
        self.child_assent_options = {
            'screening_identifier': self.caregiver_screening.screening_identifier,
            'subject_identifier': self.caregiver_child_consent.subject_identifier,
            'consent_datetime': get_utcnow(),
            'version': '1',
            'dob': (get_utcnow() - relativedelta(years=8)).date(),
            'gender': FEMALE,
            'first_name': 'TEST ONE',
            'last_name': 'TEST',
            'initials': 'TOT',
            'identity': '2345131871',
            'identity_type': 'birth_cert',
            'confirm_identity': '2345131871',
            'preg_testing': YES,
            'citizen': YES}

    def test_preg_testing_test_female_not_applicable(self):
        form_validator = PreFlourishChildAssentFormValidator(
            cleaned_data=self.child_assent_options)

        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('preg_testing', form_validator._errors)

    def test_pregnancy_applicable_above_12(self):
        self.child_assent_options['dob'] = (get_utcnow() - relativedelta(years=14)).date()
        self.child_assent_options.update({'preg_testing': NOT_APPLICABLE})

        form_validator = PreFlourishChildAssentFormValidator(
            cleaned_data=self.child_assent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('preg_testing', form_validator._errors)

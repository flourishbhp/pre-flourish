from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import YES, OTHER
from model_mommy import mommy

from ..form_validators import PreFlourishConsentFormValidator


@tag('sc')
class TestSubjectConsentForm(TestCase):

    def setUp(self):

        self.screening_identifier = 'ABC12345'
        self.study_child_identifier = '1234DCD'
        self.caregiver_screening = mommy.make_recipe(
            'pre_flourish.preflourishsubjectscreening', )

        self.consent_options = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'version': 1,
            'dob': (get_utcnow() - relativedelta(years=25)).date(),
            'first_name': 'TEST ONE',
            'last_name': 'TEST',
            'initials': 'TOT',
            'identity': '123425678',
            'confirm_identity': '123425678',
            'citizen': YES}

    def test_consent_dob_less_than_18years(self):
        self.consent_options.update({'dob': (get_utcnow() - relativedelta(years=16)).date()})
        form_validator = PreFlourishConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('dob', form_validator._errors)

    def test_recruit_source_OTHER_source_other_required(self):
        self.consent_options.update(
            {'recruit_source': OTHER,
             'recruit_source_other': None})
        form_validator = PreFlourishConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recruit_source_other', form_validator._errors)

    def test_recruit_source_OTHER_source_other_provided(self):
        self.consent_options.update(
            {'recruit_source': OTHER,
             'recruit_source_other': 'None'})
        form_validator = PreFlourishConsentFormValidator(
            cleaned_data=self.consent_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_first_name_last_name_valid(self):
        self.consent_options.update(
            {'first_name': 'TEST BONE',
             'last_name': 'TEST',
             'initials': 'TOT'})
        form_validator = PreFlourishConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('initials', form_validator._errors)

    def test_first_name_last_name_invalid(self):
        self.consent_options.update(
            {'first_name': 'TEST ONE',
             'last_name': 'TEST',
             'initials': 'TOT'})
        form_validator = PreFlourishConsentFormValidator(
            cleaned_data=self.consent_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_first_name_invalid(self):
        self.consent_options.update(
            {'first_name': 'TEST ONE BEST',
             'last_name': 'TEST',
             'initials': 'TOT'})
        form_validator = PreFlourishConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('first_name', form_validator._errors)

    def test_dob_match_screening_invalid(self):
        self.caregiver_screening.screening_identifier = 'ABC12345'
        self.caregiver_screening.caregiver_age = 30
        self.caregiver_screening.save()
        self.consent_options.update(
            {'dob': (get_utcnow() - relativedelta(years=25)).date()})
        form_validator = PreFlourishConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('dob', form_validator._errors)

    def test_dob_match_screening_valid(self):
        self.caregiver_screening.screening_identifier = 'ABC12345'
        self.caregiver_screening.caregiver_age = 25
        self.caregiver_screening.save()
        self.consent_options.update(
            {'dob': (get_utcnow() - relativedelta(years=25)).date()})
        try:
            form_validator = PreFlourishConsentFormValidator(
                cleaned_data=self.consent_options)
        except Exception:
            self.fail("Value should not fail")

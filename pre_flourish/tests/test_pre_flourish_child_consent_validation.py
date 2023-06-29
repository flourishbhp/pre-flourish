from django.test import TestCase, tag
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy
from edc_base import get_utcnow
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.core.exceptions import ValidationError
from pre_flourish.form_validators.caregiver_child_consent_form_validator import PreFlourishCaregiverChildConsentFormValidator

@tag('cc')
class TestChildConsentForm(TestCase):

    def test_dob_invalid(self):
        caregiver_child_consent = {

            'child_dob':datetime.now().date()
        }

        form_validator = PreFlourishCaregiverChildConsentFormValidator(
                cleaned_data=caregiver_child_consent)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('child_dob', form_validator._errors)

    def test_dob_valid(self):
        caregiver_child_consent = {

            'child_dob':(get_utcnow() - relativedelta(years=7)).date(),
        }

        form_validator = PreFlourishCaregiverChildConsentFormValidator(
                cleaned_data=caregiver_child_consent)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')


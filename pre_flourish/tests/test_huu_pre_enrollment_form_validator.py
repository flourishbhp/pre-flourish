from django.core.exceptions import ValidationError
from django.test import tag, TestCase
from edc_constants.constants import NO

from pre_flourish.form_validators import HuuPreEnrollmentFormValidator


@tag('huu_pre_enrollment')
class TestHUUPreEnrollment(TestCase):
    def test_validate_gestational_age_no_age_but_knows_age_in_weeks_raises_error(self):
        cleaned_data = {'knows_gest_age': 'yes_weeks'}
        form_validator = HuuPreEnrollmentFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError):
            form_validator.validate_gestational_age()

    def test_validate_gestational_age_no_age_but_knows_age_in_months_raises_error(self):
        cleaned_data = {'knows_gest_age': 'yes_months'}
        form_validator = HuuPreEnrollmentFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError):
            form_validator.validate_gestational_age()

    def test_validate_gestational_age_knows_no_age_but_provides_age_raises_error(self):
        cleaned_data = {
            'knows_gest_age': NO,
            'gestational_age_weeks': 2,
            'gestational_age_months': 3,
        }
        form_validator = HuuPreEnrollmentFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError):
            form_validator.validate_gestational_age()

    def test_validate_gestational_age_valid_entries_does_not_raise_error(self):
        cleaned_data = {
            'knows_gest_age': 'yes_weeks',
            'gestational_age_weeks': 2,
        }
        form_validator = HuuPreEnrollmentFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate_gestational_age()
        except ValidationError:
            self.fail("validate_gestational_age() raised ValidationError unexpectedly!")

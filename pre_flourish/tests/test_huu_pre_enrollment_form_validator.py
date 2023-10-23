from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_constants.constants import YES

from pre_flourish.form_validators import HuuPreEnrollmentFormValidator


@tag('huu_pre_enrollment')
class TestHUUPreEnrollment(TestCase):

    def test_both_weeks_and_months_provided(self):
        form_data = {
            'knows_gest_age': YES, 'gestational_age_weeks': 12,
            'gestational_age_months': 2}
        form = HuuPreEnrollmentFormValidator(cleaned_data=form_data)
        with self.assertRaises(ValidationError):
            form.clean()

    def test_neither_weeks_nor_months_provided(self):
        form_data = {
            'knows_gest_age': YES, 'gestational_age_weeks': None,
            'gestational_age_months': None}
        form = HuuPreEnrollmentFormValidator(cleaned_data=form_data)
        with self.assertRaises(ValidationError):
            form.clean()

    def test_only_weeks_provided(self):
        form_data = {
            'knows_gest_age': YES, 'gestational_age_weeks': 12,
            'gestational_age_months': None}
        form = HuuPreEnrollmentFormValidator(cleaned_data=form_data)
        form.validate_gestational_age()

    def test_only_months_provided(self):
        form_data = {
            'knows_gest_age': YES, 'gestational_age_weeks': None,
            'gestational_age_months': 3}
        form = HuuPreEnrollmentFormValidator(cleaned_data=form_data)
        form.validate_gestational_age()

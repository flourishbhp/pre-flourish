import datetime
from django.core.exceptions import ValidationError
from edc_constants.choices import YES

from edc_form_validators import FormValidator


class HuuPreEnrollmentFormValidator(FormValidator):

    def clean(self):

        required_fields = ['child_hiv_result', 'child_test_date']

        for field in required_fields:
            self.required_if(
                YES,
                field='child_hiv_docs',
                field_required=field)

        self.required_if(
            YES,
            field='knows_gest_age',
            field_required='gestational_age')

        self.required_if(
            YES,
            field='breastfed',
            field_required='months_breastfeed')



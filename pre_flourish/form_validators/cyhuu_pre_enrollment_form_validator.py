from edc_constants.constants import YES
from edc_form_validators import FormValidator


class CyhuuPreEnrollmentFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            YES,
            field='hiv_docs',
            field_required='hiv_test_result')

        self.required_if(
            YES,
            field_required='hiv_docs',
            field='biological_mother'
        )

        self.required_if(
            YES,
            field='hiv_docs',
            field_required='hiv_test_date'
        )

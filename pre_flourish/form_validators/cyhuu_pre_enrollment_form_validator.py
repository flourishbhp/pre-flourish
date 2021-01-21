from edc_constants.constants import YES
from edc_form_validators import FormValidator


class CyhuuPreEnrollmentFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            YES,
            field='hiv_docs',
            field_required='hiv_test_result')

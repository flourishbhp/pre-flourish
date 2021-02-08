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

        child_dob = self.cleaned_data.get('child_dob')

        start = datetime.datetime.strptime("2005-05-01", "%Y-%m-%d").date()
        end = datetime.datetime.strptime("2012-11-01", "%Y-%m-%d").date()

        if child_dob < start or child_dob > end:
            message = {'child_dob':
                       'DOB must be between 1-May-2005 and 1-Nov-2012'}
            self._errors.update(message)
            raise ValidationError(message)



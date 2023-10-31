from django.core.exceptions import ValidationError
from edc_constants.choices import YES
from edc_constants.constants import NO

from edc_form_validators import FormValidator


class HuuPreEnrollmentFormValidator(FormValidator):

    def clean(self):
        cleaned_data = super().clean()
        required_fields = ['child_hiv_result', 'child_test_date']

        for field in required_fields:
            self.required_if(
                YES,
                field='child_hiv_docs',
                field_required=field)

        self.required_if(
            YES,
            field='breastfed',
            field_required='months_breastfeed')

        self.validate_gestational_age()

        return cleaned_data

    def validate_gestational_age(self):
        gestational_age_weeks = self.cleaned_data.get('gestational_age_weeks')
        gestational_age_months = self.cleaned_data.get('gestational_age_months')
        knows_gest_age = self.cleaned_data.get('knows_gest_age')

        if knows_gest_age == 'yes_weeks' and not gestational_age_weeks:
            raise ValidationError('Please enter either weeks, not both.')
        elif knows_gest_age == 'yes_months' and not gestational_age_months:
            raise ValidationError('Please enter either months, not both.')
        elif knows_gest_age == NO and (gestational_age_weeks or gestational_age_months):
            raise ValidationError('Gestational age should not be entered if caregiver '
                                  'does not know it.')

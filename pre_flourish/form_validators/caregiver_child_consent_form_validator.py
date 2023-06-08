from edc_base.utils import age, get_utcnow
from edc_constants.choices import FEMALE, MALE, YES, NO, NOT_APPLICABLE
from flourish_form_validations.form_validators import CaregiverChildConsentFormValidator
from django.core.exceptions import ValidationError

class PreFlourishCaregiverChildConsentFormValidator(CaregiverChildConsentFormValidator):

    child_dataset_model = 'flourish_child.childdataset'

    preg_women_screening_model = 'flourish_caregiver.screeningpregwomen'

    delivery_model = 'flourish_caregiver.maternaldelivery'


    def validate_previously_enrolled(self, cleaned_data):
        pass


    def validate_child_years_more_tha_12yrs_at_jun_2025(self, cleaned_data):
        pass

    def validate_child_knows_status(self, cleaned_data):

        child_dob = cleaned_data.get('child_dob')
        consent_date = cleaned_data.get('consent_datetime')

        if child_dob and consent_date:
            child_age = age(child_dob, consent_date).years
            if child_age < 16 and cleaned_data.get(
                    'child_knows_status') in [YES, NO]:
                msg = {'child_knows_status':
                           'Child is less than 16 years'}
                self._errors.update(msg)
                raise ValidationError(msg)
            elif child_age >= 16 and cleaned_data.get(
                    'child_knows_status') == NOT_APPLICABLE:
                msg = {'child_knows_status':
                           'This field is applicable'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def preg_not_required(self):
        pass

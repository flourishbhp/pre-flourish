from datetime import datetime
from edc_base.utils import age, get_utcnow
from edc_constants.choices import FEMALE, MALE, YES, NO, NOT_APPLICABLE
from flourish_form_validations.form_validators import CaregiverChildConsentFormValidator
from django.core.exceptions import ValidationError

class PreFlourishCaregiverChildConsentFormValidator(CaregiverChildConsentFormValidator):
    def clean(self):
        super().clean()
        self.validate_child_age(cleaned_data=self.cleaned_data)
        self.validate_child_dob_is_today(cleaned_data=self.cleaned_data)

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

    def validate_child_age(self, cleaned_data):
        child_dob = cleaned_data.get('child_dob', None)
        child_age = age(child_dob, get_utcnow()).years

        if child_age and child_age < 7:
            msg = {'child_dob':
                           'Child must be 7 years or older'}
            self._errors.update(msg)
            raise ValidationError(msg)
        
    def validate_child_dob_is_today(self,cleaned_data):

        child_dob = cleaned_data.get('child_dob', None)
        current_date = datetime.now().date()

        if child_dob and child_dob >= current_date:
            msg = {'child_dob':
                           'Child age must be an older date not today'}
            self._errors.update(msg)
            raise ValidationError(msg)
        



from flourish_form_validations.form_validators import CaregiverChildConsentFormValidator


class PreFlourishCaregiverChildConsentFormValidator(CaregiverChildConsentFormValidator):

    child_dataset_model = 'flourish_child.childdataset'

    preg_women_screening_model = 'flourish_caregiver.screeningpregwomen'

    delivery_model = 'flourish_caregiver.maternaldelivery'


    def validate_previously_enrolled(self, cleaned_data):
        pass


    def validate_child_years_more_tha_12yrs_at_jun_2025(self, cleaned_data):
        pass

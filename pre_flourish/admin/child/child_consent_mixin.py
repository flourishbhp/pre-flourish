from django.contrib import admin

from pre_flourish.forms import PreFlourishCaregiverChildConsentForm
from pre_flourish.models import PreFlourishCaregiverChildConsent


class ChildConsentMixin:
    model = PreFlourishCaregiverChildConsent
    form = PreFlourishCaregiverChildConsentForm

    extra = 0
    max_num = 3

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'first_name',
                'last_name',
                'gender',
                'child_dob',
                'child_test',
                'child_remain_in_study',
                'child_preg_test',
                'child_knows_status',
                'identity',
                'identity_type',
                'confirm_identity',
                'future_studies_contact',
                'consent_datetime'
            ]}
         ),)

    radio_fields = {'gender': admin.VERTICAL,
                    'child_test': admin.VERTICAL,
                    'child_remain_in_study': admin.VERTICAL,
                    'child_preg_test': admin.VERTICAL,
                    'child_knows_status': admin.VERTICAL,
                    'identity_type': admin.VERTICAL,
                    'future_studies_contact': admin.VERTICAL}

    class Meta:
        abstract = True

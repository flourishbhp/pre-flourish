from edc_constants.constants import MALE, FEMALE
from edc_model_admin import ModelAdminBasicMixin
from edc_model_admin import ModelAdminFormAutoNumberMixin, audit_fieldset_tuple, \
    audit_fields
from edc_model_admin import StackedInlineMixin
from django.contrib import admin
from ...models import PreFlourishCaregiverChildConsent
from ...forms import PreFlourishCaregiverChildConsentForm


class PreFlourishCaregiverChildConsentInline(StackedInlineMixin, ModelAdminFormAutoNumberMixin,
                                  admin.StackedInline):
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
                'specimen_consent',
                'consent_datetime'
            ]}
         ),)

    radio_fields = {'gender': admin.VERTICAL,
                    'child_test': admin.VERTICAL,
                    'child_remain_in_study': admin.VERTICAL,
                    'child_preg_test': admin.VERTICAL,
                    'child_knows_status': admin.VERTICAL,
                    'identity_type': admin.VERTICAL,
                    'specimen_consent': admin.VERTICAL,
                    'future_studies_contact': admin.VERTICAL}
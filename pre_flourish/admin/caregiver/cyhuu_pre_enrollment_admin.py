from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin

from ...admin_site import pre_flourish_admin
from ...forms import CyhuuPreEnrollmentForm
from ...models import CyhuuPreEnrollment


@admin.register(CyhuuPreEnrollment, site=pre_flourish_admin)
class CyhuuPreEnrollmentAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CyhuuPreEnrollmentForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'biological_mother',
                'child_dob',
                'hiv_docs',
                'hiv_test_result',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'biological_mother': admin.VERTICAL,
                    'hiv_docs': admin.VERTICAL,
                    'hiv_test_result': admin.VERTICAL}

    search_fields = ['screening_identifier']

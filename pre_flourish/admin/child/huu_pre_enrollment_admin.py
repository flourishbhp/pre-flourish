from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin

from ...admin_site import pre_flourish_admin
from ...forms import HuuPreEnrollmentForm
from ...models import HuuPreEnrollment


@admin.register(HuuPreEnrollment, site=pre_flourish_admin)
class HuuPreEnrollmentAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = HuuPreEnrollmentForm

    fieldsets = (
        (None, {
            'fields': [
                'pre_flourish_visit',
                'report_datetime',
                'child_hiv_docs',
                'child_hiv_result',
                'child_test_date',
                'child_weight_kg',
                'child_height',
                'knows_gest_age',
                'gestational_age_weeks',
                'gestational_age_months',
                'premature_at_birth',
                'breastfed',
                'months_breastfeed',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'child_hiv_docs': admin.VERTICAL,
                    'child_hiv_result': admin.VERTICAL,
                    'knows_gest_age': admin.VERTICAL,
                    'premature_at_birth': admin.VERTICAL,
                    'breastfed': admin.VERTICAL}
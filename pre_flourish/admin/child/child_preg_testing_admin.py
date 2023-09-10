from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ...admin_site import pre_flourish_admin
from ...forms import ChildPregTestingForm
from ...models import PFChildPregTesting


@admin.register(PFChildPregTesting, site=pre_flourish_admin)
class ChildPregTestingAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = ChildPregTestingForm

    fieldsets = (
        (None, {
            'fields': [
                'pre_flourish_visit',
                'report_datetime',
                'test_done',
                'test_date',
                'preg_test_result',
                'comments'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'test_done': admin.VERTICAL,
                    'preg_test_result': admin.VERTICAL,}

    search_fields = 'subject_identifier'

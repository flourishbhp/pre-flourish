from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ...admin_site import pre_flourish_admin
from ...forms import PFChildHIVRapidTestCounselingForm
from ...models import PFChildHIVRapidTestCounseling


@admin.register(PFChildHIVRapidTestCounseling, site=pre_flourish_admin)
class PFChildHIVRapidTestCounselingAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = PFChildHIVRapidTestCounselingForm

    fieldsets = (
        (None, {
            'fields': [
                'pre_flourish_visit',
                'report_datetime',
                'rapid_test_done',
                'result_date',
                'result',
                'comments']}
         ), audit_fieldset_tuple)

    list_display = ('pre_flourish_visit',
                    'rapid_test_done',
                    'result')
    list_filter = ('rapid_test_done', 'result')
    search_fields = ('result_date', )
    radio_fields = {"rapid_test_done": admin.VERTICAL,
                    "result": admin.VERTICAL, }

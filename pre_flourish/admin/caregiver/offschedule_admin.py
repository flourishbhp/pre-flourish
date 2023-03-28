from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin
from ...forms.caregiver import CaregiverOffScheduleForm
from ...models.caregiver import CaregiverOffSchedule
from ...admin_site import pre_flourish_admin


@admin.register(CaregiverOffSchedule, site=pre_flourish_admin)
class CaregiverOffScheduleAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = CaregiverOffScheduleForm

    fieldsets = (
        (None, {
            'fields': [
                'schedule_name',
                'subject_identifier'
            ]}
         ), audit_fieldset_tuple)

    list_filter = ('schedule_name', 'subject_identifier',)

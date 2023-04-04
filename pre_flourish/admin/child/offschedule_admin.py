from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from pre_flourish.admin.caregiver.modeladmin_mixins import ModelAdminMixin
from pre_flourish.admin_site import pre_flourish_admin
from pre_flourish.forms import ChildOffScheduleForm
from pre_flourish.models.child import ChildOffSchedule


@admin.register(ChildOffSchedule, site=pre_flourish_admin)
class ChildOffScheduleAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = ChildOffScheduleForm

    fieldsets = (
        (None, {
            'fields': [
                'schedule_name',
                'subject_identifier'
            ]}
         ), audit_fieldset_tuple)

    list_filter = ('schedule_name', 'subject_identifier',)

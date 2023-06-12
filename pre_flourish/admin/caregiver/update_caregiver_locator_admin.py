from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from pre_flourish_follow.admin import ModelAdminMixin
from ...admin_site import pre_flourish_admin
from ...forms import UpdateCaregiverLocatorForm
from ...models import UpdateCaregiverLocator


@admin.register(UpdateCaregiverLocator, site=pre_flourish_admin)
class UpdateCaregiverLocatorAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = UpdateCaregiverLocatorForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'report_datetime',
                'is_locator_updated',
            ]}
         ), audit_fieldset_tuple)

    list_display = ('report_datetime',)

    radio_fields = {'is_locator_updated': admin.VERTICAL, }

    search_fields = ['subject_identifier']

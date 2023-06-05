from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ...admin_site import pre_flourish_admin
from ...forms import UpdateCaregiverLocatorForm
from ...models import UpdateCaregiverLocator


@admin.register(UpdateCaregiverLocator, site=pre_flourish_admin)
class UpdateCaregiverLocatorAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = UpdateCaregiverLocatorForm

    fieldsets = (
        (None, {
            'fields': [
                'pre_flourish_visit',
                'report_datetime',
                'is_locator_updated',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'is_locator_updated': admin.VERTICAL, }

    search_fields = ['subject_identifier']

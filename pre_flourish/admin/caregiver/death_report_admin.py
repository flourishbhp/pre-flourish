from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from ...admin_site import pre_flourish_admin
from ...forms import DeathReportForm
from ...models import DeathReport
from .modeladmin_mixins import ModelAdminMixin


@admin.register(DeathReport, site=pre_flourish_admin)
class DeathReportAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = DeathReportForm

    search_fields = ('subject_identifier',)

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'report_datetime',
                ]}
         ), audit_fieldset_tuple)


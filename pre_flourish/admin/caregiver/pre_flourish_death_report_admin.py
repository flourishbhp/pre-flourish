from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from ...admin_site import pre_flourish_admin
from ...forms import PreFlourishDeathReportForm
from ...models import PreFlourishDeathReport
from .modeladmin_mixins import ModelAdminMixin


@admin.register(PreFlourishDeathReport, site=pre_flourish_admin)
class PreFlourishDeathReportAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = PreFlourishDeathReportForm

    search_fields = ('subject_identifier',)

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'report_datetime',
                ]}
         ), audit_fieldset_tuple)


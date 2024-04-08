from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from edc_odk.admin import ODKActionMixin
from edc_model_admin import TabularInlineMixin


from ..admin_site import pre_flourish_admin
from ..forms import PreflourishClinicianNotesForm, PreflourishClinicianNotesImageForm
from ..models import PreFlourishClinicianNotes, ClinicianNotesImage
from .caregiver.modeladmin_mixins import CrfModelAdminMixin


class ClinicianNotesImageInline(TabularInlineMixin, admin.TabularInline):

    model = ClinicianNotesImage
    form = PreflourishClinicianNotesImageForm
    extra = 0

    fields = ('clinician_notes_image', 'image', 'user_uploaded', 'datetime_captured',
              'modified', 'hostname_created',)

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        fields = ('clinician_notes_image', 'datetime_captured',
                  'user_uploaded') + fields

        return fields


@admin.register(PreFlourishClinicianNotes, site=pre_flourish_admin)
class ClinicianNotesAdmin(ODKActionMixin, CrfModelAdminMixin,
                          admin.ModelAdmin):

    form = PreflourishClinicianNotesForm

    fieldsets = (
        (None, {
            'fields': [
                'pre_flourish_visit',], },
         ), )

    list_display = ('pre_flourish_visit', 'created',
                    'verified_by', 'is_verified',)

    inlines = [ClinicianNotesImageInline]

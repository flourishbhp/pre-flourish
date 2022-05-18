from django.contrib import admin

from ...admin_site import pre_flourish_admin
from ...forms import PreFlourishSubjectScreeningForm
from ...models import PreFlourishSubjectScreening
from .modeladmin_mixins import ModelAdminMixin


@admin.register(PreFlourishSubjectScreening, site=pre_flourish_admin)
class PreFlourishSubjectScreeningAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = PreFlourishSubjectScreeningForm
    search_fields = ['subject_identifier']

    fields = ('screening_identifier',
              'previous_subject_identifier',
              'report_datetime',
              'age_in_years',
              'has_omang',
              'has_child')

    radio_fields = {'has_omang': admin.VERTICAL,
                    'has_child': admin.VERTICAL}

    list_display = (
        'report_datetime', 'age_in_years', 'has_child', 'is_eligible', 'is_consented')

    list_filter = ('report_datetime', 'is_eligible', 'has_child', 'is_consented')

from django.contrib import admin

from ...admin_site import pre_flourish_admin
from ...forms import PreFlourishSubjectScreeningForm
from ...models import PreFlourishSubjectScreening
from .modeladmin_mixins import ModelAdminMixin


@admin.register(PreFlourishSubjectScreening, site=pre_flourish_admin)
class PreFlourishSubjectScreeningAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = PreFlourishSubjectScreeningForm
    search_fields = ['subject_identifier', 'screening_identifier']

    fields = ('screening_identifier',
              'previous_subject_identifier',
              'report_datetime',
              'caregiver_age',
              'caregiver_omang',
              'has_child',
              'willing_consent',
              'willing_assent',
              'study_interest',
              'remain_in_study')

    radio_fields = {'caregiver_omang': admin.VERTICAL,
                    'willing_consent': admin.VERTICAL,
                    'willing_assent': admin.VERTICAL,
                    'study_interest': admin.VERTICAL,
                    'has_child': admin.VERTICAL,
                    'remain_in_study': admin.VERTICAL, }

    list_display = (
        'report_datetime', 'caregiver_age', 'has_child', 'is_eligible', 'is_consented')

    list_filter = ('report_datetime', 'is_eligible', 'has_child', 'is_consented')

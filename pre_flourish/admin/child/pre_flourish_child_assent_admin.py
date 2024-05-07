from django.conf import settings
from django.contrib import admin
from django.shortcuts import reverse
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_model_admin import (
    ModelAdminFormAutoNumberMixin, ModelAdminInstitutionMixin,
    ModelAdminNextUrlRedirectMixin,
    ModelAdminReplaceLabelTextMixin)
from edc_model_admin import audit_fieldset_tuple

from ..exportaction_mixin import ExportActionMixin
from ...admin_site import pre_flourish_admin
from ...forms import PreFlourishChildAssentForm
from ...models import PreFlourishChildAssent


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormAutoNumberMixin,
                      ModelAdminRevisionMixin, ModelAdminReplaceLabelTextMixin,
                      ModelAdminInstitutionMixin, ExportActionMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'

    def redirect_url(self, request, obj, post_url_continue=None):
        url = settings.DASHBOARD_URL_NAMES.get('pre_flourish_subject_dashboard_url')

        child_subject_identifier = request.POST.get('subject_identifier', None)

        if child_subject_identifier:

            return reverse(url, args=[child_subject_identifier[:17],])

        else:
            return super().redirect_url(request, obj, post_url_continue)

    def update_variables(self, data={}):
        """ Update study identifiers to desired variable name(s).
        """
        new_data_dict = {}
        replace_idx = {'subject_identifier': 'childpid',
                       'study_maternal_identifier': 'old_matpid',
                       'study_child_identifier': 'old_childpid'}
        for old_idx, new_idx in replace_idx.items():
            try:
                new_data_dict[new_idx] = data.pop(old_idx)
            except KeyError:
                continue
        new_data_dict.update(data)
        return new_data_dict


@admin.register(PreFlourishChildAssent, site=pre_flourish_admin)
class PreFlourishChildAssentAdmin(
        ModelAdminMixin, admin.ModelAdmin):

    form = PreFlourishChildAssentForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'first_name',
                'last_name',
                'initials',
                'language',
                'is_literate',
                'witness_name',
                'dob',
                'is_dob_estimated',
                'citizen',
                'gender',
                'identity',
                'identity_type',
                'confirm_identity',
                'hiv_testing',
                'remain_in_study',
                'preg_testing')}),
        ('Review Questions', {
            'fields': (
                'consent_reviewed',
                'study_questions',
                'assessment_score',
                'consent_signature',
                'consent_copy',
                'specimen_consent',
                'consent_datetime'),
            'description': 'The following questions are directed to the interviewer.'}),
        audit_fieldset_tuple)

    radio_fields = {
        'gender': admin.VERTICAL,
        'assessment_score': admin.VERTICAL,
        'citizen': admin.VERTICAL,
        'consent_copy': admin.VERTICAL,
        'consent_reviewed': admin.VERTICAL,
        'consent_signature': admin.VERTICAL,
        'is_dob_estimated': admin.VERTICAL,
        'identity_type': admin.VERTICAL,
        'is_literate': admin.VERTICAL,
        'language': admin.VERTICAL,
        'study_questions': admin.VERTICAL,
        'remain_in_study': admin.VERTICAL,
        'hiv_testing': admin.VERTICAL,
        'preg_testing': admin.VERTICAL,
        'specimen_consent': admin.VERTICAL, }

    list_display = ('subject_identifier',
                    'verified_by',
                    'is_verified',
                    'is_verified_datetime',
                    'first_name',
                    'initials',
                    'gender',
                    'dob',
                    'consent_datetime',
                    'created',
                    'modified',
                    'user_created',
                    'user_modified')

    list_filter = ('is_verified',
                   'remain_in_study',
                   'hiv_testing',
                   'preg_testing',
                   'gender',
                   'identity_type')

    search_fields = ('subject_identifier', 'dob',)

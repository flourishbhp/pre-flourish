from django.conf import settings
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.sites.admin import ModelAdminSiteMixin
from edc_metadata import NextFormGetter
from edc_model_admin import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminInstitutionMixin,
    ModelAdminRedirectOnDeleteMixin)
from edc_model_admin import audit_fieldset_tuple
from edc_subject_dashboard import ModelAdminSubjectDashboardMixin

from .exportaction_mixin import ExportActionMixin
from ...admin_site import pre_flourish_admin
from ...forms import PreFlourishOffStudyForm
from ...models import PreFlourishOffStudy


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin,
                      ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin,
                      ModelAdminInstitutionMixin,
                      ModelAdminRedirectOnDeleteMixin,
                      ModelAdminSubjectDashboardMixin,
                      ModelAdminSiteMixin, ExportActionMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'
    next_form_getter_cls = NextFormGetter
    pre_flourish_subject_dashboard_url = 'pre_flourish_subject_dashboard_url'

    post_url_on_delete_name = settings.DASHBOARD_URL_NAMES.get(
        pre_flourish_subject_dashboard_url)

    def post_url_on_delete_kwargs(self, request, obj):
        return dict(subject_identifier=obj.subject_identifier)


@admin.register(PreFlourishOffStudy, site=pre_flourish_admin)
class PreFlourishOffStudyAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = PreFlourishOffStudyForm

    search_fields = ('subject_identifier',)

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'report_datetime',
                'offstudy_date',
                'reason',
                'reason_other',
                'comment']}
         ), audit_fieldset_tuple)

    def response_add(self, request, obj, **kwargs):
        response = self._redirector(obj)
        return response if response else super().response_add(
            request, obj)

    def response_change(self, request, obj):
        response = self._redirector(obj)
        return response if response else super().response_change(request, obj)

    def _redirector(self, obj):
        if 'P' in obj.subject_identifier:
            subject_url = 'pre_flourish_subject_dashboard_url'
            pid_parts = obj.subject_identifier.split('-')
            if len(pid_parts) == 4:
                subject_url = 'pre_flourish_child_dashboard_url'
            pre_flourish_url = reverse(
                settings.DASHBOARD_URL_NAMES.get(subject_url),
                kwargs=dict(subject_identifier=obj.subject_identifier))
            return HttpResponseRedirect(pre_flourish_url)

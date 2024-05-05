from django.conf import settings
from django.contrib import admin
from django.urls.base import reverse
from django.http import HttpResponseRedirect
from django.urls.exceptions import NoReverseMatch
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.sites.admin import ModelAdminSiteMixin
from edc_fieldsets import FieldsetsModelAdminMixin
from edc_metadata import NextFormGetter
from edc_model_admin import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin,
    FormAsJSONModelAdminMixin, ModelAdminRedirectOnDeleteMixin)
from simple_history.admin import SimpleHistoryAdmin

from edc_visit_tracking.modeladmin_mixins import (
    CrfModelAdminMixin as VisitTrackingCrfModelAdminMixin)

from ..exportaction_mixin import ExportActionMixin


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin,
                      ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                      ModelAdminInstitutionMixin,
                      ModelAdminRedirectOnDeleteMixin,
                      ModelAdminSiteMixin,
                      ExportActionMixin):

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

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'
    next_form_getter_cls = NextFormGetter


class ChildCrfModelAdminMixin(
        VisitTrackingCrfModelAdminMixin, ModelAdminMixin,
        FieldsetsModelAdminMixin, FormAsJSONModelAdminMixin,
        SimpleHistoryAdmin, admin.ModelAdmin):

    show_save_next = True
    show_cancel = True

    appointment_model = 'pre_flourish.appointment'

    post_url_on_delete_name = settings.DASHBOARD_URL_NAMES.get(
        'pre_flourish_child_dashboard_url')

    def post_url_on_delete_kwargs(self, request, obj):
        return dict(
            subject_identifier=obj.pre_flourish_visit.subject_identifier,
            appointment=str(obj.pre_flourish_visit.appointment.id))

    def view_on_site(self, obj):
        dashboard_url_name = settings.DASHBOARD_URL_NAMES.get(
            'pre_flourish_child_dashboard_url')
        try:
            url = reverse(
                dashboard_url_name, kwargs=dict(
                    subject_identifier=obj.pre_flourish_visit.subject_identifier,
                    appointment=str(obj.pre_flourish_visit.appointment.id)))
        except NoReverseMatch:
            url = super().view_on_site(obj)
        return url

    def response_add(self, request, obj, **kwargs):
        response = self._redirector(obj)
        return response if response else super().response_add(
            request, obj)

    def response_change(self, request, obj):
        response = self._redirector(obj)
        return response if response else super().response_change(request, obj)

    def _redirector(self, obj):
        if 'P' in obj.subject_identifier:
            subject_url = 'pre_flourish_child_dashboard_url'
            pre_flourish_url = reverse(
                settings.DASHBOARD_URL_NAMES.get(subject_url),
                kwargs=dict(
                    subject_identifier=obj.pre_flourish_visit.subject_identifier,
                    appointment=str(obj.pre_flourish_visit.appointment.id)))
            return HttpResponseRedirect(pre_flourish_url)

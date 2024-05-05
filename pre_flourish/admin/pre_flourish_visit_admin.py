from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_constants.constants import NO
from edc_model_admin import audit_fieldset_tuple
from edc_model_admin import ModelAdminFormAutoNumberMixin, ModelAdminInstitutionMixin, \
    ModelAdminNextUrlRedirectError, ModelAdminNextUrlRedirectMixin, \
    ModelAdminReplaceLabelTextMixin
from edc_visit_schedule.fieldsets import visit_schedule_fieldset_tuple
from edc_visit_tracking.modeladmin_mixins import VisitModelAdminMixin

from pre_flourish.admin_site import pre_flourish_admin
from pre_flourish.constants import INFANT
from .exportaction_mixin import ExportActionMixin
from ..forms import PreFlourishVisitForm
from ..models import PreFlourishVisit


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormAutoNumberMixin,
                      ModelAdminRevisionMixin, ModelAdminReplaceLabelTextMixin,
                      ModelAdminInstitutionMixin, ExportActionMixin):
    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'

    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)
        if request.GET.dict().get('next'):
            url_name = request.GET.dict().get('next').split(',')[0]
            attrs = request.GET.dict().get('next').split(',')[1:]
            options = {k: request.GET.dict().get(k)
                       for k in attrs if request.GET.dict().get(k)}
            if (obj.require_crfs == NO):
                del options['appointment']
            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')
        return redirect_url

    def update_variables(self, data={}):
        """ Update study identifiers to desired variable name(s).
        """
        new_data_dict = {}
        replace_idx = {'subject_identifier': 'childpid',
                       'study_maternal_identifier': 'old_matpid',
                       'study_child_identifier': 'old_childpid'}
        if len(data.get('subject_identifier', '').split('-')) == 3:
            replace_idx.update({'subject_identifier': 'matpid',
                                'child_subject_identifier': 'childpid', })
        for old_idx, new_idx in replace_idx.items():
            try:
                new_data_dict[new_idx] = data.pop(old_idx)
            except KeyError:
                continue
        new_data_dict.update(data)
        return new_data_dict


@admin.register(PreFlourishVisit, site=pre_flourish_admin)
class PreFlourishVisitAdmin(ModelAdminMixin, VisitModelAdminMixin, admin.ModelAdmin):
    form = PreFlourishVisitForm
    dashboard_type = INFANT

    def response_add(self, request, obj, **kwargs):
        return self._response(request, obj)

    def response_change(self, request, obj):
        return self._response(request, obj)

    def _response(self, request, obj):
        attrs = request.GET.dict().get('next').split(',')[1:]
        options = {k: request.GET.dict().get(k)
                   for k in attrs if request.GET.dict().get(k)}
        response = self._redirector(obj, options)
        return response if response else super().response_change(request, obj)

    def _redirector(self, obj, options):

        if 'P' in obj.subject_identifier:
            subject_url = 'pre_flourish_subject_dashboard_url'
            pid_parts = obj.subject_identifier.split('-')
            if len(pid_parts) == 4:
                subject_url = 'pre_flourish_child_dashboard_url'
            try:
                redirect_url = reverse(subject_url, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={subject_url}, kwargs={options}.')
            return HttpResponseRedirect(redirect_url)

    fieldsets = (
        (None, {
            'fields': [
                'appointment',
                'report_datetime',
                'reason',
                'reason_missed',
                'study_status',
                'require_crfs',
                'info_source',
                'info_source_other',
                'is_present',
                'survival_status',
                'last_alive_date',
                'comments'
            ]}),
        visit_schedule_fieldset_tuple,
        audit_fieldset_tuple
    )

    radio_fields = {
        'reason': admin.VERTICAL,
        'study_status': admin.VERTICAL,
        'require_crfs': admin.VERTICAL,
        'info_source': admin.VERTICAL,
        'is_present': admin.VERTICAL,
        'survival_status': admin.VERTICAL
    }

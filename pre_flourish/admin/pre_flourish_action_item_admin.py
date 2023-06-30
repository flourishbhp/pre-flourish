from django.conf import settings
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from edc_action_item.admin import ActionItemAdmin

from pre_flourish.admin_site import pre_flourish_admin
from pre_flourish.models import PFActionItem


class PreFlourishActionItemAdmin(ActionItemAdmin):
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


admin.site.register(PFActionItem, PreFlourishActionItemAdmin, site=pre_flourish_admin)

from django.http import HttpResponseRedirect
from django.urls import NoReverseMatch, reverse
from edc_model_admin import ModelAdminNextUrlRedirectError


class AdminRedirectMixin:

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

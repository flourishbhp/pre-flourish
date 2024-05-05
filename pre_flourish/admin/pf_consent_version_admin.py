from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from edc_base.utils import get_utcnow
from edc_fieldsets import FieldsetsModelAdminMixin
from edc_fieldsets.fieldlist import Insert
from edc_model_admin import audit_fieldset_tuple, ModelAdminNextUrlRedirectError
from edc_model_admin import ModelAdminNextUrlRedirectMixin

from .caregiver.modeladmin_mixins import ModelAdminMixin
from ..admin_site import pre_flourish_admin
from ..forms import PFConsentVersionForm
from ..models import PFConsentVersion


@admin.register(PFConsentVersion, site=pre_flourish_admin)
class PFConsentVersionAdmin(ModelAdminMixin, ModelAdminNextUrlRedirectMixin,
                            FieldsetsModelAdminMixin,
                            admin.ModelAdmin):
    form = PFConsentVersionForm

    def get_url_and_options(self, request, obj, consent_model):
        url_name = request.GET.dict().get('next').split(',')[0]
        attrs = request.GET.dict().get('next').split(',')[1:]
        options = {k: request.GET.dict().get(k)
                   for k in attrs if request.GET.dict().get(k)}
        if request.GET.get('screening_identifier'):
            consents = consent_model.objects.filter(
                screening_identifier=request.GET.get('screening_identifier'))
            consent = None
            if consents:
                consent = consents.latest('consent_datetime')
            if consent:
                url_name = settings.DASHBOARD_URL_NAMES.get(
                    'pre_flourish_screening_listboard_url')
        return url_name, options

    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)
        if obj:
            consent_model = django_apps.get_model('pre_flourish.preflourishconsent')
            url_name, options = self.get_url_and_options(request, obj, consent_model)
            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')
        return redirect_url

    fieldsets = (
        (None, {
            'fields': [
                'screening_identifier',
                'report_datetime',
                'version',
                'child_version'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'version': admin.VERTICAL,
                    'child_version': admin.VERTICAL}

    list_display = ('screening_identifier',
                    'report_datetime',
                    'version',
                    'child_version')

    conditional_fieldlists = {'is_preg': Insert(
        'child_version', after='version')}

    def is_delivery_window(self, subject_identifier):

        maternal_delivery_cls = django_apps.get_model(
            'flourish_caregiver.maternaldelivery')

        try:
            maternal_delivery_obj = maternal_delivery_cls.objects.get(
                subject_identifier=subject_identifier)
        except maternal_delivery_cls.DoesNotExist:
            return True
        else:
            return ((
                            get_utcnow().date() -
                            maternal_delivery_obj.delivery_datetime.date()).days
                    <= 3)

from django.apps import apps as django_apps
from django.contrib import admin
from django.conf import settings
from django.urls import reverse, NoReverseMatch
from edc_constants.constants import NOT_APPLICABLE
from edc_model_admin import audit_fieldset_tuple, ModelAdminNextUrlRedirectError

from ...admin_site import pre_flourish_admin
from ...forms import PreFlourishLogEntryForm
from ...models import PreFlourishLogEntry
from .exportaction_mixin import ExportActionMixin
from .modeladmin_mixins import ModelAdminMixin


@admin.register(PreFlourishLogEntry, site=pre_flourish_admin)
class PreFlourishLogEntryAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = PreFlourishLogEntryForm

    search_fields = ['study_maternal_identifier']

    fieldsets = (
        (None, {
            'fields': (
                'study_maternal_identifier',
                'prev_study',
                'call_datetime',
                'phone_num_type',
                'phone_num_success',)
        }),

        ('Subject Cell & Telephones', {
            'fields': ('cell_contact_fail',
                       'alt_cell_contact_fail',
                       'tel_contact_fail',
                       'alt_tel_contact_fail',)
        }),
        ('Subject Work Contact', {
            'fields': ('work_contact_fail',)
        }),
        ('Indirect Contact Cell & Telephone', {
            'fields': ('cell_alt_contact_fail',
                       'tel_alt_contact_fail',)
        }),
        ('Caretaker Cell & Telephone', {
            'fields': ('cell_resp_person_fail',
                       'tel_resp_person_fail')
        }),
        ('Schedule Appointment With Participant', {
            'fields': ('appt',
                       'appt_type',
                       'other_appt_type',
                       'appt_reason_unwilling',
                       'appt_reason_unwilling_other',
                       'appt_date',
                       'appt_grading',
                       'appt_location',
                       'appt_location_other',
                       'may_call',
                       'home_visit',
                       'home_visit_other',
                       'final_contact',
                       )
        }), audit_fieldset_tuple)

    radio_fields = {'appt': admin.VERTICAL,
                    'appt_type': admin.VERTICAL,
                    'appt_grading': admin.VERTICAL,
                    'appt_location': admin.VERTICAL,
                    'may_call': admin.VERTICAL,
                    'cell_contact_fail': admin.VERTICAL,
                    'alt_cell_contact_fail': admin.VERTICAL,
                    'tel_contact_fail': admin.VERTICAL,
                    'alt_tel_contact_fail': admin.VERTICAL,
                    'work_contact_fail': admin.VERTICAL,
                    'cell_alt_contact_fail': admin.VERTICAL,
                    'tel_alt_contact_fail': admin.VERTICAL,
                    'cell_resp_person_fail': admin.VERTICAL,
                    'tel_resp_person_fail': admin.VERTICAL,
                    'home_visit': admin.VERTICAL,
                    'final_contact': admin.VERTICAL,
                    }

    filter_horizontal = ('appt_reason_unwilling',)

    list_display = (
        'study_maternal_identifier', 'prev_study', 'call_datetime',)

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)

        if obj:
            study_maternal_identifier = getattr(obj, 'study_maternal_identifier', '')
        else:
            study_maternal_identifier = request.GET.get('study_maternal_identifier')

        fields = self.get_all_fields(form)

        for idx, field in enumerate(fields):
            custom_value = self.custom_field_label(study_maternal_identifier, field)

            if custom_value:
                form.base_fields[field].label = f'{idx + 1}. Why was the contact to {custom_value} unsuccessful?'
        form.custom_choices = self.phone_choices(study_maternal_identifier)
        return form

    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)
        if ('none_of_the_above' not in obj.phone_num_success
                and obj.home_visit == NOT_APPLICABLE):
            if request.GET.dict().get('next'):
                url_name = settings.DASHBOARD_URL_NAMES.get(
                    'pre_flourish_screening_listboard_url')
            options = {'study_maternal_identifier': request.GET.dict().get('study_maternal_identifier')}
            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')
        return redirect_url

    def phone_choices(self, study_identifier):
        caregiver_locator_cls = django_apps.get_model(
            'flourish_caregiver.caregiverlocator')
        field_attrs = [
            'subject_cell',
            'subject_cell_alt',
            'subject_phone',
            'subject_phone_alt',
            'subject_work_phone',
            'indirect_contact_cell',
            'indirect_contact_phone',
            'caretaker_cell',
            'caretaker_tel']

        try:
            locator_obj = caregiver_locator_cls.objects.get(
                study_maternal_identifier=study_identifier)
        except caregiver_locator_cls.DoesNotExist:
            pass
        else:
            phone_choices = ()
            for field_attr in field_attrs:
                value = getattr(locator_obj, field_attr)
                if value:
                    field_name = field_attr.replace('_', ' ')
                    value = f'{value} {field_name.title()}'
                    phone_choices += ((field_attr, value),)
            return phone_choices

    def custom_field_label(self, study_identifier, field):
        caregiver_locator_cls = django_apps.get_model(
            'flourish_caregiver.caregiverlocator')
        fields_dict = {
            'cell_contact_fail': 'subject_cell',
            'alt_cell_contact_fail': 'subject_cell_alt',
            'tel_contact_fail': 'subject_phone',
            'alt_tel_contact_fail': 'subject_phone_alt',
            'work_contact_fail': 'subject_work_phone',
            'cell_alt_contact_fail': 'indirect_contact_cell',
            'tel_alt_contact_fail': 'indirect_contact_phone',
            'cell_resp_person_fail': 'caretaker_cell',
            'tel_resp_person_fail': 'caretaker_tel'}

        try:
            locator_obj = caregiver_locator_cls.objects.get(
                study_maternal_identifier=study_identifier)
        except caregiver_locator_cls.DoesNotExist:
            pass
        else:
            attr_name = fields_dict.get(field, None)
            if attr_name:
                return getattr(locator_obj, attr_name, '')

    def get_all_fields(self, instance):
        """"
        Return names of all available fields from given Form instance.

        :arg instance: Form instance
        :returns list of field names
        :rtype: list
        """

        fields = list(instance.base_fields)

        for field in list(instance.declared_fields):
            if field not in fields:
                fields.append(field)
        return fields

    # def render_change_form(self, request, context, *args, **kwargs):
    #     context['adminform'].form.fields['log'].queryset = \
    #         Log.objects.filter(id=request.GET.get('log'))
    #     return super().render_change_form(
    #         request, context, *args, **kwargs)

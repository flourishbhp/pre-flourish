from collections import OrderedDict

from django.apps import apps as django_apps
from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_consent.actions import (
    flag_as_verified_against_paper, unflag_as_verified_against_paper)
from edc_model_admin import audit_fields, audit_fieldset_tuple, \
    ModelAdminFormAutoNumberMixin, ModelAdminInstitutionMixin, \
    ModelAdminNextUrlRedirectError, ModelAdminNextUrlRedirectMixin, \
    ModelAdminReplaceLabelTextMixin
from edc_model_admin import ModelAdminBasicMixin, ModelAdminReadOnlyMixin
from simple_history.admin import SimpleHistoryAdmin

from flourish_caregiver.admin import ConsentMixin
from .exportaction_mixin import ExportActionMixin
from ..child import PreFlourishCaregiverChildConsentInline
from ...admin_site import pre_flourish_admin
from ...forms import PreFlourishConsentForm
from ...models import PreFlourishConsent


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormAutoNumberMixin,
                      ModelAdminRevisionMixin, ModelAdminReplaceLabelTextMixin,
                      ModelAdminInstitutionMixin, ModelAdminReadOnlyMixin,
                      ExportActionMixin):
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
            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')
        return redirect_url


@admin.register(PreFlourishConsent, site=pre_flourish_admin)
class PreFlourishConsentAdmin(ModelAdminBasicMixin, ModelAdminMixin, ConsentMixin,
                              SimpleHistoryAdmin, admin.ModelAdmin):
    form = PreFlourishConsentForm
    inlines = [PreFlourishCaregiverChildConsentInline, ]

    consent_cls = django_apps.get_model('pre_flourish.preflourishconsent')

    fieldsets = (
        (None, {
            'fields': (
                'screening_identifier',
                'subject_identifier',
                'first_name',
                'last_name',
                'initials',
                'language',
                'recruit_source',
                'recruit_source_other',
                'recruitment_clinic',
                'recruitment_clinic_other',
                'is_literate',
                'witness_name',
                'dob',
                'is_dob_estimated',
                'citizen',
                'gender',
                'identity',
                'identity_type',
                'confirm_identity',
                'biological_caregiver',
                'future_contact',
                'child_consent',)}),
        ('Review Questions', {
            'fields': (
                'consent_reviewed',
                'study_questions',
                'assessment_score',
                'consent_signature',
                'consent_copy',
                'consent_datetime',),
            'description': 'The following questions are directed to the interviewer.'}),
        audit_fieldset_tuple)

    radio_fields = {
        'gender': admin.VERTICAL,
        'assessment_score': admin.VERTICAL,
        'biological_caregiver': admin.VERTICAL,
        'future_contact': admin.VERTICAL,
        'child_consent': admin.VERTICAL,
        'citizen': admin.VERTICAL,
        'consent_copy': admin.VERTICAL,
        'consent_reviewed': admin.VERTICAL,
        'consent_signature': admin.VERTICAL,
        'is_dob_estimated': admin.VERTICAL,
        'identity_type': admin.VERTICAL,
        'is_literate': admin.VERTICAL,
        'language': admin.VERTICAL,
        'recruit_source': admin.VERTICAL,
        'recruitment_clinic': admin.VERTICAL,
        'study_questions': admin.VERTICAL}

    list_display = ('subject_identifier',
                    'verified_by',
                    'is_verified',
                    'is_verified_datetime',
                    'first_name',
                    'initials',
                    'gender',
                    'dob',
                    'consent_datetime',
                    'recruit_source',
                    'recruitment_clinic',
                    'created',
                    'modified',
                    'user_created',
                    'user_modified')
    list_filter = ('language',
                   'is_verified',
                   'is_literate',
                   'identity_type')
    search_fields = ('subject_identifier', 'dob',)

    def get_actions(self, request):
        super_actions = super().get_actions(request)

        if ('pre_flourish.change_preflourishconsent'
                in request.user.get_group_permissions()):
            consent_actions = [
                flag_as_verified_against_paper,
                unflag_as_verified_against_paper]

            # Add actions from this ModelAdmin.
            actions = (self.get_action(action) for action in consent_actions)
            # get_action might have returned None, so filter any of those out.
            actions = filter(None, actions)

            actions = self._filter_actions_by_permissions(request, actions)
            # Convert the actions into an OrderedDict keyed by name.
            actions = OrderedDict(
                (name, (func, name, desc))
                for func, name, desc in actions
            )

            super_actions.update(actions)

        return super_actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=obj, **kwargs)
        if 'screening_identifier' in request.GET:
            screening_identifier = request.GET.get('screening_identifier')
            subject_identifier = self.get_subject_identifier(screening_identifier)
            if subject_identifier:
                initial_values = self.prepare_initial_values_based_on_subject(
                    subject_identifier=subject_identifier)
                form.previous_instance = initial_values
        return form

    def prepare_initial_values_based_on_subject(self, subject_identifier):
        return [self.prepare_subject_consent(subject_identifier)]

    def get_difference(self, model_objs, obj=None):
        cc_ids = obj.preflourishcaregiverchildconsent_set.values_list(
            'subject_identifier', 'version')
        consent_version_obj = self.consent_version_obj(
            obj.screening_identifier)
        child_version = getattr(consent_version_obj, 'child_version', None)
        return [x for x in model_objs if (
            x.subject_identifier, x.version) not in cc_ids or x.version != child_version]

    def get_readonly_fields(self, request, obj=None):
        return (super().get_readonly_fields(request, obj=obj) +
                audit_fields)

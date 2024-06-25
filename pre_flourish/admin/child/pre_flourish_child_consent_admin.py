from functools import partialmethod

from django.apps import apps as django_apps
from django.contrib import admin
from django.db.models import OuterRef, Q, Subquery
from edc_model_admin import ModelAdminFormAutoNumberMixin, StackedInlineMixin

from flourish_caregiver.admin import ConsentMixin
from .child_consent_mixin import ChildConsentMixin
from .model_admin_mixins import ModelAdminMixin
from ...admin_site import pre_flourish_admin
from ...models import PreFlourishCaregiverChildConsent


class PreFlourishCaregiverChildConsentInline(StackedInlineMixin,
                                             ModelAdminFormAutoNumberMixin,
                                             ChildConsentMixin,
                                             ConsentMixin,
                                             admin.StackedInline):
    caregiver_consent_cls = django_apps.get_model('pre_flourish.preflourishconsent')

    consent_cls = django_apps.get_model(
        'pre_flourish.preflourishcaregiverchildconsent')

    consent_version_cls = django_apps.get_model('pre_flourish.pfconsentversion')

    def get_formset(self, request, obj=None, **kwargs):
        screening_identifier = request.GET.get('screening_identifier')
        initial = []

        if screening_identifier:
            caregiver_consent = self.get_caregiver_consents(screening_identifier)
            if caregiver_consent:
                subject_identifier = caregiver_consent.latest(
                    'consent_datetime').subject_identifier
                initial = self.prepare_initial_values_based_on_subject(
                    obj, subject_identifier)
        formset = super().get_formset(request, obj=obj, **kwargs)
        formset.form = self.auto_number(formset.form)
        formset.__init__ = partialmethod(formset.__init__, initial=initial)
        return formset

    def prepare_initial_values_based_on_subject(self, obj, subject_identifier):
        return [self.prepare_subject_consent(consent) for consent in
                self.consents_filtered_by_subject(obj, subject_identifier)]

    def consents_filtered_by_subject(self, obj, subject_identifier):
        consents = self.consent_cls.objects.filter(
            subject_consent__subject_identifier=subject_identifier).order_by(
            'consent_datetime')
        if obj:
            consents = consents.filter(
                version=getattr(obj, 'version', None))
            subquery = consents.filter(
                subject_identifier=OuterRef('subject_identifier')).order_by(
                '-version').values('version')[:1]
            consents = consents.filter(version=Subquery(subquery))
            consents = set([c.subject_identifier for c in self.get_difference(
                consents, obj)])
        return consents

    def get_child_reconsent_extra(self, request):
        screening_identifier = request.GET.get('screening_identifier')
        subject_identifier = request.GET.get('subject_identifier')

        consent_version_obj = self.consent_version_obj(screening_identifier)
        if consent_version_obj and getattr(consent_version_obj, 'child_version', None):
            child_consent_objs = self.consent_cls.objects.filter(
                subject_consent__subject_identifier=subject_identifier,
                version=consent_version_obj.child_version)
            if not child_consent_objs:
                return 1
        return 0

    def get_difference(self, model_objs, obj=None):
        cc_ids = obj.preflourishcaregiverchildconsent_set.values_list(
            'subject_identifier', 'version')
        consent_version_obj = self.consent_version_obj(
            obj.screening_identifier)
        child_version = getattr(consent_version_obj, 'child_version', None)
        return [x for x in model_objs if (
            x.subject_identifier, x.version) not in cc_ids or x.version != child_version]

    def get_extra(self, request, obj=None, **kwargs):

        extra = (super().get_extra(request, obj, **kwargs) +
                 self.get_child_reconsent_extra(request))
        screening_identifier = request.GET.get('screening_identifier')
        if screening_identifier:
            caregiver_consent = self.get_caregiver_consents(screening_identifier)
            if caregiver_consent:
                caregiver_child_consents = set(
                    list(caregiver_consent.latest('consent_datetime')
                         .preflourishcaregiverchildconsent_set.all()
                         .values_list('subject_identifier', flat=True)))
                if not obj:
                    extra = len(caregiver_child_consents)

        return extra

    def get_caregiver_consents(self, screening_identifier=None):
        return self.caregiver_consent_cls.objects.filter(
            screening_identifier=screening_identifier)

    def consent_version_obj(self, screening_identifier=None):
        try:
            consent_version_obj = self.consent_version_cls.objects.get(
                screening_identifier=screening_identifier)
        except self.consent_version_cls.DoesNotExist:
            return None
        else:
            return consent_version_obj


@admin.register(PreFlourishCaregiverChildConsent, site=pre_flourish_admin)
class PreFlourishCaregiverChildConsentAdmin(ModelAdminMixin, ChildConsentMixin,
                                            admin.ModelAdmin):
    list_display = ('subject_identifier',
                    'verified_by',
                    'is_verified',
                    'is_verified_datetime',
                    'first_name',
                    'last_name',
                    'gender',
                    'child_dob',
                    'consent_datetime',
                    'created',
                    'modified',
                    'user_created',
                    'user_modified')

    list_filter = ('is_verified',
                   'gender',
                   'child_remain_in_study',
                   'child_knows_status',
                   'child_preg_test',
                   'identity_type')

    search_fields = ['subject_identifier',
                     'subject_consent__subject_identifier', ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [f.name for f in self.model._meta.fields]

        return super().get_readonly_fields(request, obj)

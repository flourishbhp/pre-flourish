from django.apps import apps as django_apps
from edc_base import get_utcnow
from edc_base.utils import age
from edc_constants.constants import FEMALE, NO
from edc_metadata_rules import PredicateCollection


class PreFlourishPredicates(PredicateCollection):
    app_label = 'pre_flourish'
    visit_model = f'{app_label}.preflourishvisit'

    def func_hiv_test_required(self, visit=None, **kwargs):
        huu_preenrollment_model = django_apps.get_model(
            f'{self.app_label}.huupreenrollment')
        if visit:
            try:
                obj = huu_preenrollment_model.objects.get(
                    pre_flourish_visit=visit
                )
            except huu_preenrollment_model.DoesNotExist:
                return False
            else:
                test_age = 0
                if obj.child_test_date:
                    test_age = age(obj.child_test_date, get_utcnow())
                    test_age = test_age.years * 12 + test_age.months
                return obj.child_hiv_docs == NO or test_age > 3
        else:
            return False

    def func_hiv_rapid_test_required(self, visit=None, **kwargs):
        cyhuu_preenrollment_model = django_apps.get_model(
            f'{self.app_label}.cyhuupreenrollment')
        if visit:
            try:
                obj = cyhuu_preenrollment_model.objects.get(
                    pre_flourish_visit=visit
                )
            except cyhuu_preenrollment_model.DoesNotExist:
                return False
            else:
                return obj.hiv_docs == NO
        else:
            return False

    def fun_pre_test_required(self, visit=None, **kwargs):
        pre_flourish_child_assent_model = django_apps.get_model(
            f'{self.app_label}.preflourishchildassent')
        if hasattr(visit, 'subject_identifier'):
            try:
                obj = pre_flourish_child_assent_model.objects.get(
                    subject_identifier=visit.subject_identifier
                )
            except pre_flourish_child_assent_model.DoesNotExist:
                return False
            else:
                child_age = age(obj.dob, get_utcnow()).years
                return child_age >= 11 and obj.gender == FEMALE
        else:
            return False

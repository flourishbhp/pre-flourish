from django.apps import apps as django_apps
from edc_metadata_rules.rule_evaluator import RuleEvaluator


class PFRuleEvaluator(RuleEvaluator):

    @property
    def registered_subject_model(self):
        return django_apps.get_model('pre_flourish.preflourishregisteredsubject')

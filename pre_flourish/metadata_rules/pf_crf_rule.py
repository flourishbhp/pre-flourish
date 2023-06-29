from edc_metadata_rules import CrfRule

from pre_flourish.metadata_rules.pf_rule_evaluator import PFRuleEvaluator


class PfCrfRule(CrfRule):

    rule_evaluator_cls = PFRuleEvaluator


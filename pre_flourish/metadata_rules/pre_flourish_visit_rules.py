from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRuleGroup, register

from pre_flourish.metadata_rules.pf_crf_rule import PfCrfRule
from pre_flourish.predicates import PreFlourishPredicates

app_label = 'pre_flourish'
pc = PreFlourishPredicates()


@register()
class HuuPreEnrollmentRules(CrfRuleGroup):
    pre_test = PfCrfRule(
        predicate=pc.fun_pre_test_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.pfchildpregtesting', ])

    hiv_test_counseling = PfCrfRule(
        predicate=pc.func_hiv_test_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.pfchildhivrapidtestcounseling', ])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.huupreenrollmentrules'


@register()
class ChyuuPreEnrollmentRules(CrfRuleGroup):
    hiv_test_counseling = PfCrfRule(
        predicate=pc.func_hiv_rapid_test_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.pfhivrapidtestcounseling', ])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.cyhuupreenrollment'

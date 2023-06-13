from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register

from pre_flourish.predicates import PreFlourishPredicates

app_label = 'pre_flourish'
pc = PreFlourishPredicates()


@register()
class HuuPreEnrollmentRules(CrfRuleGroup):
    pre_test = CrfRule(
        predicate=pc.fun_pre_test_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.pfchildpregtesting', ])

    hiv_test = CrfRule(
        predicate=pc.func_hiv_test_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.pfinfanthivtesting', ])

    hiv_test_counseling = CrfRule(
        predicate=pc.func_hiv_test_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.pfchildhivrapidtestcounseling', ])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.huupreenrollmentrules'

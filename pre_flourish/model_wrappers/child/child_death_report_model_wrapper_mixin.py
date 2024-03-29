from flourish_dashboard.model_wrappers.child_death_report_model_wrapper_mixin import \
    ChildDeathReportModelWrapperMixin as BaseChildDeathReportModelWrapperMixin
from .child_death_report_model_wrapper import ChildDeathReportModelWrapper


class ChildDeathReportModelWrapperMixin(BaseChildDeathReportModelWrapperMixin):
    child_death_report_model_wrapper_cls = ChildDeathReportModelWrapper

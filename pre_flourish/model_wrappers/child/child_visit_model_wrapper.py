from django.conf import settings

from flourish_dashboard.model_wrappers.child_visit_model_wrapper import \
    ChildVisitModelWrapper as VisitModelWrapper


class ChildVisitModelWrapper(VisitModelWrapper):
    model = 'pre_flourish.preflourishchildvisit'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'pre_flourish_child_dashboard_url')

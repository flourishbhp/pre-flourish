from django.conf import settings
from edc_data_manager.models import DataActionItem


class PFDataActionItem(DataActionItem):

    class Meta:
        proxy = True

    @property
    def dashboard_url(self):
        if self.subject_type == 'infant':
            return settings.DASHBOARD_URL_NAMES.get('pre_flourish_child_dashboard_url')
        return settings.DASHBOARD_URL_NAMES.get('pre_flourish_subject_dashboard_url')

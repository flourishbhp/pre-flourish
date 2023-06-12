from edc_action_item.model_mixins.action_model_mixin import ActionModelMixin
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_identifier.managers import SubjectIdentifierManager
from edc_search.model_mixins import SearchSlugModelMixin

from flourish_prn.models import DeathReportModelMixin
from pre_flourish.action_items import MATERNAL_DEATH_STUDY_ACTION


class PreFlourishDeathReport(ActionModelMixin, SiteModelMixin,
                             SearchSlugModelMixin, DeathReportModelMixin, BaseUuidModel):
    tracking_identifier_prefix = 'MO'

    action_name = MATERNAL_DEATH_STUDY_ACTION

    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.subject_identifier,)

    natural_key.dependencies = ['sites.Site']

    class Meta:
        app_label = 'pre_flourish'
        verbose_name = 'Death Report'

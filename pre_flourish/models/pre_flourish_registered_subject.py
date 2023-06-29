from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager, SiteModelMixin
from edc_registration.managers import RegisteredSubjectManager
from edc_registration.model_mixins import RegisteredSubjectModelMixin


class PreFlourishRegisteredSubject(RegisteredSubjectModelMixin, SiteModelMixin,
                                   BaseUuidModel):
    on_site = CurrentSiteManager()

    objects = RegisteredSubjectManager()

    def natural_key(self):
        return super().natural_key()

    natural_key.dependencies = ['sites.Site']

    class Meta:
        app_label = 'pre_flourish'

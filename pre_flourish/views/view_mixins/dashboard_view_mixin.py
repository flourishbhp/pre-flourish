from django.apps import apps as django_apps
from django.contrib import messages
from flourish_dashboard.views.view_mixin.dashboard_view_mixin import DashboardViewMixin \
    as BaseDashboardViewMixin


class DashboardViewMixin(BaseDashboardViewMixin):

    child_offstudy_model = 'pre_flourish.preflourishchildoffstudy'

    caregiver_offstudy_model = 'pre_flourish.preflourishoffstudy'

    @property
    def caregiver_offstudy_cls(self):
        return django_apps.get_model(self.caregiver_offstudy_model)

    def require_offstudy(self, offstudy_visit_obj, subject_identifier):
        pass

    def get_assent_object_or_message(
            self, child_age=None, subject_identifier=None, version=None):
        pass

    def get_consent_version_object_or_message(self, screening_identifier=None):
        pass

    def get_continued_consent_object_or_message(self, child_age=None,
                                                subject_identifier=None):
        pass

    def is_delivery_window(self, subject_identifier):

        pass

    def get_consent_from_version_form_or_message(self, subject_identifier,
                                                 screening_identifier):

        pass

    def get_offstudy_or_message(
            self, model_cls, action_item, subject_identifier, msg, trigger=True):
        try:
            model_cls.objects.get(
                subject_identifier=subject_identifier)
        except model_cls.DoesNotExist:
            self.action_cls_item_creator(
                trigger=trigger,
                subject_identifier=subject_identifier,
                action_cls=model_cls,
                action_type=action_item)
        if trigger:
            messages.add_message(self.request, messages.ERROR, msg)

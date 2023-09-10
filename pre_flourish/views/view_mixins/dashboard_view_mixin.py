from flourish_dashboard.views.view_mixin.dashboard_view_mixin import DashboardViewMixin \
    as BaseDashboardViewMixin


class DashboardViewMixin(BaseDashboardViewMixin):

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
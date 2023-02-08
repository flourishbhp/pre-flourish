from django.apps import apps as django_apps
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.views import DashboardView as BaseDashboardView
from edc_navbar import NavbarViewMixin
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin

from pre_flourish.model_wrappers import ChildAppointmentModelWrapper, \
    ChildConsentModelWrapper, ActionItemModelWrapper, ChildVisitModelWrapper, \
    PreflourishCaregiverLocatorModelWrapper, CaregiverChildConsentModelWrapper


class DashboardView(EdcBaseViewMixin, SubjectDashboardViewMixin,
                    NavbarViewMixin, BaseDashboardView):
    dashboard_url = 'pre_flourish_child_dashboard_url'
    dashboard_template = 'pre_flourish_child_dashboard_template'
    appointment_model = 'pre_flourish.appointment'
    appointment_model_wrapper_cls = ChildAppointmentModelWrapper
    consent_model = 'flourish_child.childdummysubjectconsent'
    consent_model_wrapper_cls = ChildConsentModelWrapper
    action_item_model_wrapper_cls = ActionItemModelWrapper
    navbar_name = 'pre_flourish_dashboard'
    navbar_selected_item = 'pre_flourish_child_subjects'
    subject_locator_model = 'flourish_caregiver.caregiverlocator'
    visit_model_wrapper_cls = ChildVisitModelWrapper
    subject_locator_model_wrapper_cls = PreflourishCaregiverLocatorModelWrapper
    mother_infant_study = True
    infant_links = False
    maternal_links = True
    maternal_dashboard_include_value = "flourish_dashboard/child_subject/dashboard/caregiver_dashboard_links.html"
    special_forms_include_value = 'pre_flourish/caregiver/dashboard/special_forms.html'

    def get_subject_locator_or_message(self):
        """
        Overridden to stop system from generating subject locator
        action items for child.
        """
        pass

    @property
    def caregiver_child_consent(self):
        child_consent_cls = django_apps.get_model(
            'pre_flourish.preflourishcaregiverchildconsent')

        child_consent = child_consent_cls.objects.filter(
            subject_identifier=self.subject_identifier).latest('consent_datetime')

        if child_consent:
            return CaregiverChildConsentModelWrapper(child_consent)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            caregiver_child_consent=self.caregiver_child_consent, )

        return context

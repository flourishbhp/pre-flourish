from django.apps import apps as django_apps
from edc_base.view_mixins import EdcBaseViewMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.views.generic.base import ContextMixin
from edc_registration.models import RegisteredSubject
from edc_dashboard.views import DashboardView as BaseDashboardView
from edc_navbar import NavbarViewMixin
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin
from flourish_dashboard.model_wrappers import MaternalRegisteredSubjectModelWrapper
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from pre_flourish.model_wrappers import ChildAppointmentModelWrapper, \
    ChildConsentModelWrapper, ActionItemModelWrapper, ChildVisitModelWrapper, \
    PreflourishCaregiverLocatorModelWrapper, CaregiverChildConsentModelWrapper


class CaregiverRegisteredSubjectCls(ContextMixin):

    @property
    def caregiver_registered_subject(self):
        try:
            caregiver_registered_subject = RegisteredSubject.objects.get(
                subject_identifier=self.caregiver_subject_identifier)
        except RegisteredSubject.DoesNotExist:
            raise ValidationError(
                "Registered subject for the mother is expected to exist.")
        else:
            return MaternalRegisteredSubjectModelWrapper(
                caregiver_registered_subject)

    @property
    def caregiver_subject_identifier(self):
        subject_identifier = self.kwargs.get('subject_identifier').split('-')
        subject_identifier.pop()
        caregiver_subject_identifier = '-'.join(subject_identifier)
        return caregiver_subject_identifier


class DashboardView(EdcBaseViewMixin, SubjectDashboardViewMixin,
                    NavbarViewMixin, BaseDashboardView, CaregiverRegisteredSubjectCls):
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
    maternal_dashboard_include_value = 'pre_flourish/child/dashboard/caregiver_dashboard_links.html'
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

    def set_current_schedule(self, onschedule_model_obj=None,
                             schedule=None, visit_schedule=None,
                             is_onschedule=True):

        if onschedule_model_obj:
            if is_onschedule:
                self.current_schedule = schedule
                self.current_visit_schedule = visit_schedule
                self.current_onschedule_model = onschedule_model_obj
            else:
                model_name = f'pre_flourish.{onschedule_model_obj._meta.model_name}'
                visit_schedule, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                    model_name, onschedule_model_obj.schedule_name)
                self.current_schedule = schedule
                self.current_visit_schedule = visit_schedule
                self.current_onschedule_model = onschedule_model_obj
            self.onschedule_models.append(onschedule_model_obj)
            self.visit_schedules.update(
                {visit_schedule.name: visit_schedule})

    def get_onschedule_model_obj(self, schedule):
        try:
            return schedule.onschedule_model_cls.objects.get(
                subject_identifier=self.subject_identifier,
                schedule_name=schedule.name)
        except ObjectDoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            caregiver_child_consent=self.caregiver_child_consent,
            schedule_names=[getattr(model, 'schedule_name') for model in self.onschedule_models]
        )
        return context

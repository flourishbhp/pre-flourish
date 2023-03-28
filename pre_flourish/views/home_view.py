from django.apps import apps as django_apps
from django.views.generic import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin


class HomeView(EdcBaseViewMixin, NavbarViewMixin, TemplateView):
    template_name = 'pre_flourish/home.html'
    navbar_name = 'pre_flourish_dashboard'
    navbar_selected_item = 'home'

    screening_model = 'pre_flourish.preflourishsubjectscreening'
    consent_model = 'pre_flourish.preflourishconsent'
    child_consent_model = 'pre_flourish.preflourishcaregiverchildconsent'
    child_assent_model = 'pre_flourish.preflourishchildassent'

    @property
    def screening_cls(self):
        return django_apps.get_model(self.screening_model)

    @property
    def consent_cls(self):
        return django_apps.get_model(self.consent_model)

    @property
    def child_consent_cls(self):
        return django_apps.get_model(self.child_consent_model)

    @property
    def child_assent_cls(self):
        return django_apps.get_model(self.child_assent_model)

    @property
    def total_consents(self):
        return self.consent_cls.objects.values_list(
            'subject_identifier').distinct().count()

    @property
    def total_screenings(self):
        return self.screening_cls.objects.values_list(
            'screening_identifier').distinct().count()

    @property
    def total_child_consents(self):
        return self.child_consent_cls.objects.values_list(
            'subject_identifier').distinct().count()

    @property
    def total_child_assent(self):
        return self.child_assent_cls.objects.values_list(
            'subject_identifier').distinct().count()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            total_child_assent=self.total_child_assent,
            total_child_consents=self.total_child_consents,
            total_screenings=self.total_screenings,
            total_consents=self.total_consents,
        )
        return context

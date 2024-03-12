from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from ...model_wrappers import PreflourishCaregiverLocatorModelWrapper, \
    PreFlourishMaternalScreeningModelWrapper


class PreFlourishCaregiverLocatorListBoardView(NavbarViewMixin, EdcBaseViewMixin,
                                               ListboardFilterViewMixin,
                                               SearchFormViewMixin,
                                               ListboardView):
    listboard_template = 'pre_flourish_caragiver_locator_listboard_template'
    listboard_url = 'pre_flourish_caregiver_locator_listboard_url'
    listboard_panel_style = 'info'
    listboard_fa_icon = "fa-user-plus"
    model = 'flourish_caregiver.caregiverlocator'
    model_wrapper_cls = PreflourishCaregiverLocatorModelWrapper
    navbar_name = 'pre_flourish_dashboard'
    navbar_selected_item = 'pre_flourish_caregiver_locator'
    paginate_by = 10
    search_form_url = 'pre_flourish_caregiver_locator_listboard_url'

    log_entry_model = 'pre_flourish_follow.preflourishlogentry'

    @property
    def log_entry_cls(self):
        return django_apps.get_model(self.log_entry_model)

    @property
    def call_log_model_objs(self):
        log_entries = self.log_entry_cls.objects.values_list(
            'study_maternal_identifier', flat=True)

        return set(list(log_entries))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_wrapped_queryset(self, queryset):
        """Returns a list of wrapped model instances.
        """
        object_list = []
        for obj in queryset:
            wrapped_obj = self.model_wrapper_cls(obj)
            wrapped_obj.subject_screening_wrapper = (
                PreFlourishMaternalScreeningModelWrapper)
            object_list.append(wrapped_obj)
        return object_list

    def get_queryset(self):
        """
        This study is for prev. BCCP participants only, hence they are being
        collected from the caregiver locator whose subject identifier starts with
        066-

        Returns:
            Queryset with BCCP participants
        """
        participants = super().get_queryset().filter(
            study_maternal_identifier__istartswith='066'
        )

        return participants

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            maternal_locator_add_url=self.model_cls().get_absolute_url())
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('screening_identifier'):
            options.update(
                {'screening_identifier': kwargs.get('screening_identifier')})
        if kwargs.get('study_maternal_identifier'):
            options.update(
                {'study_maternal_identifier': kwargs.get('study_maternal_identifier')})
        options.update(
            {'study_maternal_identifier__in': self.call_log_model_objs})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if search_term:
            q = Q(study_maternal_identifier__iexact=search_term)
        return q
